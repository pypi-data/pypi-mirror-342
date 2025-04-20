import re
from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel, ValidationError, computed_field, model_validator, Field
from transliterate import translit  # type: ignore

from shop_system_models.consts.enums import ShopStatuses
from shop_system_models.deployment_api.request.nocodb import NocoDBConfig
from shop_system_models.deployment_api.request.services import ProjectConfiguration
from shop_system_models.deployment_api.request.tasks import Task
from shop_system_models.deployment_api.response.shops import ShopCategoryResponse


class Location(BaseModel):
    latitude: float
    longitude: float
    address: str


class CreateShop(BaseModel):
    name: str
    categories: List[ShopCategoryResponse] = []
    locations: Optional[List[Location]] = []
    contact_email: str
    template_id: str
    orders_chat_id: int = 0
    friendly_name: str = ''
    contact_phone: Optional[str] = ''
    bot_token: Optional[str] = ''
    zone: Optional[int] = None

    @model_validator(mode='before')
    def set_friendly_name_and_format_name(cls, values: dict):
        name = values.get('name', '')
        if len(name) > 35:
            raise ValueError('Shop name too long; must be less than 35 symbols')

        if not values.get('friendly_name'):
            values['friendly_name'] = name.strip().strip("-")

        transliterated_name = translit(name, 'ru', reversed=True) if name else ''
        no_whitespaces_and_underscores = transliterated_name.replace(' ', '-').replace('_', '-')
        no_double_dashes = re.sub(r'-{2,}', '-', no_whitespaces_and_underscores)
        to_lowercase = no_double_dashes.lower()
        no_special_characters = re.sub(r'[^a-z0-9_-]', '', to_lowercase)
        formatted_name = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', no_special_characters)

        values['name'] = formatted_name
        return values


class Shop(CreateShop):
    # КОНСТАНТЫ ИЗ CONFIG
    WEB_APP_URL: str = ''
    FRONTEND_HOST: str = ''

    placeholder: Optional[Union[ShopStatuses, Any]] = ShopStatuses.deploying
    tasks: List[Task] = []
    language: str = 'RU'
    nocodb_config: NocoDBConfig = NocoDBConfig()

    search_enabled: Optional[bool] = False
    warehouse_accounting: Optional[bool] = False
    weekly_reports: Optional[bool] = True
    orders_history_chat_id: Optional[int] = None
    topic_chat_id: Optional[int] = None
    premium_expiration_date: Optional[datetime] = None
    broadcast_messages_count: Optional[int] = 0
    web_app_url: str = Field(default_factory=lambda: Shop.WEB_APP_URL)

    blocked: bool = False
    block_reason: str = ""

    @computed_field  # type: ignore
    @property
    def sheet_link(self) -> Optional[str]:
        if self.nocodb_config and self.nocodb_config.nocodb_project_id:
            return f"{self.FRONTEND_HOST}/dashboard/#/nc/{self.nocodb_config.nocodb_project_id}"
        return None


class ShopDB(Shop):
    id: str
    tg_admin_id: int = 0
    is_changeable: Optional[bool] = True
    order_process: str = "The-devs.Shop.CreateOrder"
    nocodb_config: NocoDBConfig = NocoDBConfig()
    preview_url: Optional[str] = None
    views_id: List[str] = []

    @computed_field  # type: ignore
    @property
    def configuration(self) -> ProjectConfiguration:
        return ProjectConfiguration(
            shop_name=self.name
        )


class UpdateFromProcess(BaseModel):
    nocodb_config: NocoDBConfig
    language: str
