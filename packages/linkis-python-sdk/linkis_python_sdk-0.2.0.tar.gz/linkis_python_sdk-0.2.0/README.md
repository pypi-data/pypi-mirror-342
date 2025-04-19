# Linkis Python SDK

Linkis Python SDK是与[Apache Linkis](https://linkis.apache.org/)服务交互的Python客户端库。该SDK提供了简便的接口，用于执行代码并获取结果，支持同步和异步操作。

Linkis Python SDK is the Python client library for interacting with [Apache Linkis](https://linkis.apache.org/) services. This SDK provides convenient interfaces for executing code and retrieving results, supporting both synchronous and asynchronous operations.

[![PyPI version](https://badge.fury.io/py/linkis-python-sdk.svg)](https://badge.fury.io/py/linkis-python-sdk)

[![Python Version](https://img.shields.io/pypi/pyversions/linkis-python-sdk.svg)](https://pypi.org/project/linkis-python-sdk/)

## 安装

## Installation

```bash
pip install linkis-python-sdk
```

## 功能特点

## Features

- 支持同步和异步客户端
- 支持结果缓存
- 提供数据过滤、排序和分页功能
- 轻松将结果转换为Pandas DataFrame

- Support for synchronous and asynchronous clients
- Result caching capabilities
- Data filtering, sorting, and pagination
- Easy conversion of results to Pandas DataFrame

## 使用示例

## Usage Examples

### 同步客户端

### Synchronous Client

```python
from linkis_python_sdk.client import LinkisClient
from linkis_python_sdk.config.config import LinkisConfig

# 创建配置
# Create configuration
config = LinkisConfig(
    base_url="http://your-linkis-server/api/rest_j/v1",
    username="your_username",
    password="your_password"
)

# 创建客户端
# Create client
client = LinkisClient(config)

# 执行代码
# Execute code
code = "SELECT * FROM my_table LIMIT 10"
query_req = {
    "columns": [{"column": "id"}, {"column": "name"}],
    "filters": [{"column": "age", "operator": "gt", "value": 18}],
    "orderbys": [{"column": "id", "ascending": True}],
    "page": 1,
    "page_size": 10
}
data, total, error = client.execute_code(
    code=code,
    query_req=query_req,
    engine_type="spark",
    run_type="sql"
)

print(f"Total records: {total}")
print(f"Data: {data}")
```

### 异步客户端

### Asynchronous Client

```python
import asyncio
from linkis_python_sdk.asyncio.client import LinkisClient
from linkis_python_sdk.config.config import LinkisConfig

async def main():
    # 创建配置
    # Create configuration
    config = LinkisConfig(
        base_url="http://your-linkis-server/api/rest_j/v1",
        username="your_username",
        password="your_password"
    )
    
    # 创建异步客户端
    # Create asynchronous client
    client = LinkisClient(config)
    
    # 执行代码
    # Execute code
    code = "SELECT * FROM my_table LIMIT 10"
    query_req = {
        "columns": [{"column": "id"}, {"column": "name"}],
        "filters": [{"column": "age", "operator": "gt", "value": 18}],
        "orderbys": [{"column": "id", "ascending": True}],
        "page": 1,
        "page_size": 10
    }
    data, total, error = await client.execute_code(
        code=code,
        query_req=query_req,
        engine_type="spark",
        run_type="sql"
    )
    
    print(f"Total records: {total}")
    print(f"Data: {data}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 带缓存的执行

## Execution with Caching

SDK还支持使用Redis缓存执行结果，以提高性能：

The SDK also supports caching execution results with Redis to improve performance:

```python
from redis import ConnectionPool
from linkis_python_sdk.client import LinkisClient
from linkis_python_sdk.config.config import LinkisConfig

# 创建Redis连接池
# Create Redis connection pool
redis_pool = ConnectionPool(host="localhost", port=6379, db=0)

# 创建配置
# Create configuration
config = LinkisConfig(
    base_url="http://your-linkis-server/api/rest_j/v1",
    username="your_username",
    password="your_password"
)

# 创建带缓存的客户端
# Create client with caching
client = LinkisClient(
    linkis_conf=config,
    r_pool=redis_pool,
    cache_expire=1800,  # 缓存过期时间（秒）/ Cache expiration time (seconds)
    cache_code_prefix="linkis:codecache"  # 缓存键前缀 / Cache key prefix
)

# 执行带缓存的代码
# Execute code with caching
data, total, error = client.execute_code_with_cache(
    code="SELECT * FROM my_table LIMIT 10",
    query_req={"columns": [{"column": "id"}, {"column": "name"}]},
    engine_type="spark",
    run_type="sql"
)
```

## 依赖项

## Dependencies

- Python >= 3.9
- requests
- pandas
- redis
- aiohttp

## 开发贡献

## Development and Contribution

欢迎为Linkis Python SDK做出贡献！请参阅[PUBLISH.md](PUBLISH.md)了解如何构建和发布该包。
Contributions to the Linkis Python SDK are welcome! Please refer to [PUBLISH.md](PUBLISH.md) for information on how to build and publish the package.

## 许可证

## License

该项目采用[Apache License 2.0](LICENSE)许可证。

This project is licensed under the [Apache License 2.0](LICENSE). 