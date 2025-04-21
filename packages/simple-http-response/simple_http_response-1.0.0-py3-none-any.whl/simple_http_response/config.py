from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


Header = Annotated[str, Field(
    description='Header in the format "Key: Value"',
    pattern=r'^[a-zA-Z0-9-_]+:\s?.+$',
    min_length=1,
    max_length=256
)]


class Config(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True, env_nested_delimiter='__')

    HOST: str = Field(default='127.0.0.1', min_length=1, description='host of the server')
    PORT: int = Field(default=8080, gt=0, description='port of the server')
    ENDPOINT: str = Field(default='/', min_length=1, description='endpoint of the server')
    CODE: int = Field(default=200, gt=0, description='http code to answer requests with')
    HEADER: list[Header] = Field(default_factory=list, description='headers of the server response')
    BODY: str = Field(default='', description='body of the server response')
    LOG_LEVEL: Literal['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO',
        description='Logging level of the server'
    )
    METHOD: list[Literal['GET', 'POST', 'PUT', 'DELETE']] = Field(
        default=['GET', 'POST', 'PUT', 'DELETE'],
        description='HTTP method of the server'
    )
