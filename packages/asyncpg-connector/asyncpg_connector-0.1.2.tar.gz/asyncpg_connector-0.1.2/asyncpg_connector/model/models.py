from pydantic import BaseModel


class ConnectorConfig(BaseModel):
    """
    Configuration for the asyncpg connector.
    """

    host: str
    port: int
    user: str
    password: str
    database: str
    ssl: bool = False
