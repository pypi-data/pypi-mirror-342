import hashlib
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Protocol, Dict, Any, List

import requests
from redis import ConnectionPool, Redis
from redis.lock import Lock
from requests import Session

from linkis_python_sdk.config.config import LinkisConfig
from linkis_python_sdk.core import data_resolve
from linkis_python_sdk.model.model import ResultSet


class ILinkisClient(Protocol):

    def execute_code(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        ...

    def execute_code_with_cache(
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

    def execute_code(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        try:
            req_session = requests.Session()
            self._login(req_session)
            result_files = self._running_code_task(req_session, code, engine_type, run_type)
            if len(result_files) <= 0:
                raise ValueError("no data files")
            result_sets = self._query_result_set(req_session, result_files)
            data, total = data_resolve.resolve_data(result_sets, query_req)
            return data, total, ""
        except Exception as e:
            logging.exception(e)
            return [], 0, str(e)

    def execute_code_with_cache(
            self,
            code: str,
            query_req: Dict[str, Any],
            engine_type: str,
            run_type: str,
    ) -> (List[Dict[str, Any]], int, str):
        try:
            if not self.redis_pool:
                raise RuntimeError("cache config is not set")
            with Redis(connection_pool=self.redis_pool) as redis_cli:
                req_session = requests.Session()
                self._login(req_session)
                code_digest = hashlib.md5(code.encode()).hexdigest()
                cache_key = f"{self.cache_code_prefix}:{code_digest}"
                if cache_val := redis_cli.get(cache_key):
                    result_files = json.loads(cache_val)
                else:
                    result_files = self._building_cache(
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
                result_sets = self._query_result_set(req_session, result_files)
                data, total = data_resolve.resolve_data(result_sets, query_req)
                return data, total, ""
        except Exception as e:
            logging.exception(e)
            return [], 0, str(e)

    def _query_result_set(self, req_session: Session, result_files: List[str]) -> List[ResultSet]:
        with ThreadPoolExecutor() as executor:
            result_sets = executor.map(
                lambda x: self._query_data_file(*x),
                [(req_session, {"charset": "utf8", "path": rf}) for rf in result_files]
            )
            return list(result_sets)

    def _query_data_file(self, req_session: Session, params: Dict[str, Any]) -> ResultSet:
        file_resp = req_session.get(url=f"{self.linkis_conf.base_url}/filesystem/openFile", params=params)
        file_data = file_resp.json()
        if file_data.get("status", -2) != 0:
            raise ValueError(file_data["message"])
        result_set = ResultSet.from_response(file_data.get('data', {}))
        return result_set

    def _login(self, req_session: Session):
        login_body = {
            "userName": self.linkis_conf.username,
            "password": self.linkis_conf.password
        }
        login_resp = req_session.post(url=f"{self.linkis_conf.base_url}/user/login", json=login_body)
        login_data = login_resp.json()
        if login_data.get("status", -2) != 0:
            raise ValueError(login_data["message"])

    def _building_cache(
            self,
            req_session: Session,
            cache_key: str,
            code: str,
            engine_type: str,
            run_type: str,
            code_digest: str,
            redis_cli: Redis
    ) -> List[str]:
        lock_name = f"{self.cache_code_prefix}:building:{code_digest}"
        with Lock(redis_cli, name=lock_name, timeout=300, blocking_timeout=60) as _:
            if cache_val := redis_cli.get(cache_key):
                result_files = json.loads(cache_val)
            else:
                result_files = self._running_code_task(req_session, code, engine_type, run_type)
                redis_cli.setex(cache_key, self.cache_expire, json.dumps(result_files, ensure_ascii=False))
            return result_files

    def _running_code_task(
            self,
            req_session: Session,
            code: str,
            engine_type: str,
            run_type: str,
    ) -> List[str]:
        exec_data = self._submit(req_session, code, engine_type, run_type)
        task_id, exec_id = exec_data["data"].get("taskID"), exec_data["data"].get("execID")
        task = self._waiting_task_finish(req_session, task_id)
        if task.get("status", "Unknown") != "Succeed":
            raise ValueError(task["errDesc"])
        result_files = self._get_file_dir(req_session, task)
        return result_files

    def _get_file_dir(self, req_session: Session, task: Dict[str, Any]) -> List[str]:
        url = f"{self.linkis_conf.base_url}/filesystem/getDirFileTrees"
        params = {'path': task["resultLocation"]}
        dir_resp = req_session.get(url=url, params=params)
        dir_data = dir_resp.json()
        if dir_data.get("status", -2) != 0:
            raise ValueError(dir_data["message"])
        result_files = []
        children = dir_data.get("data", {}).get("dirFileTrees", {}).get('children', [])
        for child in children:
            if child.get('isLeaf'):
                result_files.append(child.get('path'))
        return result_files

    def _submit(
            self,
            req_session: Session,
            code: str,
            engine_type: str,
            run_type: str
    ) -> Dict[str, Any]:
        submit_body = {
            "executionContent": {"code": code, "runType": run_type},
            "labels": {"engineType": engine_type, "userCreator": f"{self.linkis_conf.username}-IDE"}
        }
        exec_resp = req_session.post(url=f"{self.linkis_conf.base_url}/entrance/submit", json=submit_body)
        exec_data = exec_resp.json()
        if exec_data.get("status", -2) != 0:
            raise ValueError(exec_data["message"])
        return exec_data

    def _waiting_task_finish(self, req_session: Session, task_id: int) -> Dict[str, Any]:
        while True:
            task_resp = req_session.get(f"{self.linkis_conf.base_url}/jobhistory/{task_id}/get")
            task_data = task_resp.json()
            if task_data.get("status", -2) != 0:
                raise ValueError(task_data["message"])
            task_status = task_data.get("data", {}).get("task", {}).get("status", "Unknown")
            if task_status in self.ready_statuses:
                task = task_data["data"]["task"]
                break
            time.sleep(1)
        return task
