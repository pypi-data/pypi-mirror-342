from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class ShopTemplate(BaseModel):
    template_id: str
    name: str
    description: Optional[str] = ''
    bot_url: str
    language: str

    @field_validator('bot_url')
    def url_validation(cls, bot_url):
        if bot_url.startswith('http://') or bot_url.startswith('https://'):
            return bot_url
        raise HTTPException(status_code=400, detail=f'Invalid bot_url: {bot_url}')
