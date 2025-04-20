from shop_system_models.deployment_api.users import UserModel


class UserResponseModel(UserModel):
    id: str
    is_service: bool = False
