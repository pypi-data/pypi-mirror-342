from typing import List, Optional

from shop_system_models.consts.enums import UserRoles
from shop_system_models.consts.languages import TG_LANGUAGES_MAPPING
from pydantic import BaseModel, field_validator, model_validator, computed_field


class ReferralUser(BaseModel):
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    tg_id: int


class User(BaseModel):
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    tg_id: int
    tg_language: str = ''  # language_code from TG

    @computed_field  # type: ignore
    @property
    def language(self) -> str:
        return TG_LANGUAGES_MAPPING.get(self.tg_language, 'EN')


class UserDB(User):
    invited_by_id: Optional[str] = None
    invited_by_user: Optional[ReferralUser] = None
    cache_key: Optional[str] = None


class UserExtended(UserDB):
    SHOPS_LIMIT: int = 0  # сюда потом в рантайме подставишь значение из конфига

    roles: List[str] = []  # 'shop_admin:<shop_id>' or 'admin'
    shops_available: int = SHOPS_LIMIT

    @field_validator('roles')
    def if_admin(cls, roles: list):
        for role in roles:
            if role == UserRoles.admin.value:
                return [UserRoles.admin.value]
        return roles

    @field_validator('shops_available')
    def admin_limit(cls, shops_available, model):
        roles = model.data['roles']
        for role in roles:
            if role == UserRoles.admin.value:
                return 10
        return shops_available
