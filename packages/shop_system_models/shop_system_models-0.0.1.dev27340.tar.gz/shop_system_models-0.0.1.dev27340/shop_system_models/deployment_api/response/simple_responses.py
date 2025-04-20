from typing import List, Optional


from shop_system_models.deployment_api.request.services import ServiceConfig
from shop_system_models.deployment_api.request.shop_templates import ShopTemplate
from shop_system_models.deployment_api.request.shops import CreateShop, Shop, ShopDB
from shop_system_models.deployment_api.request.tasks import Task
from shop_system_models.deployment_api.request.users import User, UserExtended
from pydantic import BaseModel

from shop_system_models.deployment_api.response.general import ListResponseModel


class BasicResponse(BaseModel):
    message: str





class ServiceConfigResponse(ServiceConfig):
    id: str


class CreateShopResponse(CreateShop):
    id: str


class ShopResponse(Shop):
    id: str
    preview_url: Optional[str] = None


class ShopResponseId(ShopDB):
    id: str


class ShopsListResponseModel(ListResponseModel):
    shops: List[ShopResponseId]


class ShopDBResponse(ShopDB):
    id: str


class TaskResponse(Task):
    id: str


class UserResponse(UserExtended):
    id: str
    invited_users: Optional[List[User]] = None
    cache_key: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str


class ShopTemplateResponse(ShopTemplate):
    id: str
