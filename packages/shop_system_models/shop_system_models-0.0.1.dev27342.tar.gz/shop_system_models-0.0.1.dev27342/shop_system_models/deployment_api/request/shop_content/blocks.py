from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


def link_validation(link: str) -> str:
    if not link.startswith('http://') and not link.startswith('https://'):
        raise HTTPException(status_code=400, detail=f'Invalid link: {link}')
    return link


class LinkBlocks(BaseModel):
    contacts: Optional[str] = None
    info: Optional[str] = None

    @field_validator('contacts', 'info')
    def link_validation(cls, value: str) -> str:
        if value:
            return link_validation(link=value)
        return value
