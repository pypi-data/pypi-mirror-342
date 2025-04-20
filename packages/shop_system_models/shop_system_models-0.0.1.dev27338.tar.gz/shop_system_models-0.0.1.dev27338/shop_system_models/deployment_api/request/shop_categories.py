from typing import Optional

from pydantic import BaseModel


class ShopCategory(BaseModel):
    name: str
    description: Optional[str] = None
    preview_url: Optional[str] = None
