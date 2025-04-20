import re

from pydantic import BaseModel, Field, field_validator


class WebAppUrlUpdateRequest(BaseModel):
    web_app_url: str = Field(..., description="The URL of the telegram web app")

    @field_validator("web_app_url")
    def validate_web_app_url(cls, value):
        pattern = r"^https://t\.me/[A-Za-z0-9_]+/[A-Za-z0-9_]+$"
        if not re.match(pattern, value):
            raise ValueError("web_app_url must follow the pattern: 'https://t.me/{bot_name}/{webapp_name}', where bot_name and webapp_name can vary.")
        return value