from typing import Optional

from shop_system_models.consts.enums import ServiceNames
from pydantic import BaseModel, computed_field


class ServiceConfig(BaseModel):
    name: ServiceNames
    version: Optional[str] = 'latest'

    class Config:
        use_enum_values = True


class ProjectConfiguration(BaseModel):
    shop_name: str

    # Константы для URL — будут задаваться в рантайме
    SHOP_BOT_URL: str = ''
    SHOP_API_URL: str = ''
    SHOP_APP_URL: str = ''

    @computed_field  # type: ignore
    @property
    def shop_bot_url(self) -> str:
        return f"{self.SHOP_BOT_URL}/{self.shop_name}"

    @computed_field  # type: ignore
    @property
    def shop_api_url(self) -> str:
        return f"{self.SHOP_API_URL}/{self.shop_name}"

    @computed_field  # type: ignore
    @property
    def shop_url(self) -> str:
        return f"{self.SHOP_APP_URL}/{self.shop_name}"
