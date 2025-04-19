import asyncio
import hashlib
import json
import logging
from typing import Protocol, Dict, Any, List

from aiohttp import ClientSession, CookieJar
from redis.asyncio import Redis, ConnectionPool
from redis.asyncio.lock import Lock

from linkis_python_sdk.config.config import LinkisConfig
from linkis_python_sdk.core import data_resolve
from linkis_python_sdk.model.model import ResultSet


class ILinkisClient(Protocol):

    async def execute_code(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        ...

    async def execute_code_with_cache(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        ...


class LinkisClient:

    def __init__(
            self,
            linkis_conf: LinkisConfig,
            r_pool: ConnectionPool = None,
            cache_expire: int = 60 * 30,
            cache_code_prefix: str = "linkis:codecache"
    ):
        self.linkis_conf = linkis_conf
        self.ready_statuses = ["Succeed", "Failed", "Timeout", "Cancelled", "Unknown"]
        self.redis_pool = r_pool
        self.cache_expire = cache_expire
        self.cache_code_prefix = cache_code_prefix

    async def execute_code(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        try:
            async with ClientSession(cookie_jar=CookieJar(unsafe=True)) as req_session:
                await self._login(req_session)
                result_files = await self._running_code_task(req_session, code, engine_type, run_type)
                if len(result_files) <= 0:
                    raise ValueError("no data files")
                result_sets = await self._query_result_set(req_session, result_files)
                data, total = await self._resolve_data(result_sets, query_req)
                return data, total, ""
        except Exception as e:
            logging.exception(e)
            return [], 0, str(e)

    async def execute_code_with_cache(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        try:
            if not self.redis_pool:
                raise RuntimeError("cache config is not set")
            async with Redis(connection_pool=self.redis_pool) as redis_cli:
                async with ClientSession(cookie_jar=CookieJar(unsafe=True)) as req_session:
                    await self._login(req_session)
                    code_digest = hashlib.md5(code.encode()).hexdigest()
                    cache_key = f"{self.cache_code_prefix}:{code_digest}"
                    if cache_val := await redis_cli.get(cache_key):
                        result_files = json.loads(cache_val)
                    else:
                        result_files = await self._building_cache(
                            req_session,
                            cache_key,
                            code,
                            engine_type,
                            run_type,
                            code_digest,
                            redis_cli,
                        )
                    if len(result_files) <= 0:
                        raise ValueError("no data files")
                    result_sets = await self._query_result_set(req_session, result_files)
                    data, total = await self._resolve_data(result_sets, query_req)
                    return data, total, ""
        except Exception as e:
            logging.exception(e)
            return [], 0, str(e)

    async def _resolve_data(
            self,
            result_sets: List[ResultSet],
            query_req: Dict[str, Any]
    ) -> (List[Dict[str, Any]], int):
        data, total_records = data_resolve.resolve_data(result_sets, query_req)
        return data, total_records

    async def _query_result_set(self, req_session: ClientSession, result_files: List[str]) -> List[ResultSet]:
        result_sets = await asyncio.gather(*[
            self._query_data_file(req_session, params={"charset": "utf8", "path": rf})
            for rf in result_files
        ])
        return result_sets

    async def _query_data_file(self, req_session: ClientSession, params: Dict[str, Any]) -> ResultSet:
        async with req_session.get(url=f"{self.linkis_conf.base_url}/filesystem/openFile", params=params) as file_resp:
            file_data = await file_resp.json()
            if file_data.get("status", -2) != 0:
                raise ValueError(file_data["message"])
            result_set = ResultSet.from_response(file_data.get('data', {}))
        return result_set

    async def _login(self, req_session: ClientSession):
        login_body = {
            "userName": self.linkis_conf.username,
            "password": self.linkis_conf.password
        }
        async with req_session.post(url=f"{self.linkis_conf.base_url}/user/login", json=login_body) as login_resp:
            login_data = await login_resp.json()
            if login_data.get("status", -2) != 0:
                raise ValueError(login_data["message"])

    async def _building_cache(
            self,
            req_session: ClientSession,
            cache_key: str,
            code: str,
            engine_type: str,
            run_type: str,
            code_digest: str,
            redis_cli: Redis
    ) -> List[str]:
        lock_name = f"{self.cache_code_prefix}:building:{code_digest}"
        async with Lock(redis_cli, name=lock_name, timeout=300, blocking_timeout=60) as _:
            if cache_val := await redis_cli.get(cache_key):
                result_files = json.loads(cache_val)
            else:
                result_files = await self._running_code_task(req_session, code, engine_type, run_type)
                await redis_cli.setex(cache_key, self.cache_expire, json.dumps(result_files, ensure_ascii=False))
            return result_files

    async def _running_code_task(
            self,
            req_session: ClientSession,
            code: str,
            engine_type: str,
            run_type: str,
    ) -> List[str]:
        exec_data = await self._submit(req_session, code, engine_type, run_type)
        task_id, exec_id = exec_data["data"].get("taskID"), exec_data["data"].get("execID")
        task = await self._waiting_task_finish(req_session, task_id)
        if task.get("status", "Unknown") != "Succeed":
            raise ValueError(task["errDesc"])
        result_files = await self._get_file_dir(req_session, task)
        return result_files

    async def _get_file_dir(self, req_session: ClientSession, task: Dict[str, Any]) -> List[str]:
        url = f"{self.linkis_conf.base_url}/filesystem/getDirFileTrees"
        params = {'path': task["resultLocation"]}
        async with req_session.get(url=url, params=params) as dir_resp:
            dir_data = await dir_resp.json()
            if dir_data.get("status", -2) != 0:
                raise ValueError(dir_data["message"])
            result_files = []
            children = dir_data.get("data", {}).get("dirFileTrees", {}).get('children', [])
            for child in children:
                if child.get('isLeaf'):
                    result_files.append(child.get('path'))
            return result_files

    async def _submit(
            self,
            req_session: ClientSession,
            code: str,
            engine_type: str,
            run_type: str
    ) -> Dict[str, Any]:
        submit_body = {
            "executionContent": {"code": code, "runType": run_type},
            "labels": {"engineType": engine_type, "userCreator": f"{self.linkis_conf.username}-IDE"}
        }
        async with req_session.post(url=f"{self.linkis_conf.base_url}/entrance/submit", json=submit_body) as exec_resp:
            exec_data = await exec_resp.json()
            if exec_data.get("status", -2) != 0:
                raise ValueError(exec_data["message"])
            return exec_data

    async def _waiting_task_finish(self, req_session: ClientSession, task_id: int) -> Dict[str, Any]:
        while True:
            async with req_session.get(f"{self.linkis_conf.base_url}/jobhistory/{task_id}/get") as task_resp:
                task_data = await task_resp.json()
                if task_data.get("status", -2) != 0:
                    raise ValueError(task_data["message"])
                task_status = task_data.get("data", {}).get("task", {}).get("status", "Unknown")
                if task_status in self.ready_statuses:
                    task = task_data["data"]["task"]
                    break
            await asyncio.sleep(1)
        return task
