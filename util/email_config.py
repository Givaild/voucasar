from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, field_validator
import os

class EmailConfig(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp-relay.brevo.com"
    MAIL_FROM_NAME: str = "IntegraCAR"
    
    FRONTEND_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra="ignore"
    )

    @field_validator("MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_FROM", "MAIL_FROM_NAME", "FRONTEND_URL", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

settings = EmailConfig()