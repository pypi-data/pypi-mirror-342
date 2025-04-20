from pydantic import BaseModel

from shop_system_models.deployment_api.request.premium import PremiumPlanTypes


class PremiumLinkResponseModel(BaseModel):
    shop_name: str
    premium_type: str
    link: str


class PremiumPlanType(BaseModel):
    price: int
    final_price: int
    type: PremiumPlanTypes
