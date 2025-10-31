from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

class ConfigEnv(BaseSettings):
    # PostgreSQL Configuration
    postgres_host: Optional[str] = Field(None, json_schema_extra={"env": "POSTGRES_HOST"})
    postgres_user: Optional[str] = Field(None, json_schema_extra={"env": "POSTGRES_USER"})
    postgres_password: Optional[str] = Field(None, json_schema_extra={"env": "POSTGRES_PASSWORD"})
    postgres_port: Optional[str] = Field(None, json_schema_extra={"env": "POSTGRES_PORT"})
    postgres_db: Optional[str] = Field(None, json_schema_extra={"env": "POSTGRES_DB"})
    # Google API Key
    google_api_key: Optional[str] = Field(None, json_schema_extra={"env": "GOOGLE_API_KEY"})
    
    model_config = ConfigDict(env_file=".env", extra="allow")  # ✅ Updated

config_env = ConfigEnv()