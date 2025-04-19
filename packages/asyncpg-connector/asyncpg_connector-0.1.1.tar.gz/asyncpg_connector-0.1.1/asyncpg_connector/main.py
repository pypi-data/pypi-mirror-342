import asyncio
import asyncpg
from typing import Union
from asyncpg_connector.error import DatabaseConnectionError
from asyncpg_connector.model import ConnectorConfig


class AsyncpgConnector:
    def __init__(self, connect_config: Union[ConnectorConfig, dict]):
        if isinstance(connect_config, dict):
            self.connect_config = ConnectorConfig(**connect_config)
        else:
            self.connect_config = connect_config
        self.conn = None

    async def __aenter__(self):
        try:
            self.conn = await asyncpg.connect(**self.connect_config.model_dump())
            return self
        except Exception as e:
            raise DatabaseConnectionError(f"Database connection failed:{e}")

    async def __aexit__(self, *args):
        await asyncio.gather(self.conn.close(timeout=10), return_exceptions=True)

    def __await__(self):
        return self.__aenter__().__await__()
