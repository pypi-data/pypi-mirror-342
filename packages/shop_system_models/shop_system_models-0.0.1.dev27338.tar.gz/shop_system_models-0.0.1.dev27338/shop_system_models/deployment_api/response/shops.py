from datetime import datetime
from typing import List, Optional


from shop_system_models.deployment_api.request.nocodb import NocoDBConfig
from shop_system_models.deployment_api.request.shop_categories import ShopCategory
from shop_system_models.deployment_api.request.shop_content.blocks import LinkBlocks
from shop_system_models.deployment_api.request.shop_content.delivery_types import DeliveryTypeResponse
from shop_system_models.deployment_api.request.shop_content.payment_methods import PaymentMethodResponse
from pydantic import BaseModel, Field


class ContentDataResponseModel(BaseModel):
    blocks: Optional[LinkBlocks]
    delivery_types: Optional[List[DeliveryTypeResponse]]
    payment_methods: Optional[List[PaymentMethodResponse]]


class ShopDetails(BaseModel):
    shop_id: str
    shop_name: str
    friendly_name: str
    shop_language: Optional[str] = 'RU'
    shop_api_url: str
    contact_phone: str
    contact_email: str
    orders_chat_id: int # orders_management_chat_id
    orders_history_chat_id: Optional[int] = None
    topic_chat_id: Optional[int] = None
    bot_url: str
    bot_token: str
    placeholder: str
    order_process: str
    search_enabled: bool = False
    warehouse_accounting: bool = False
    nocodb_config: Optional[NocoDBConfig] = None
    nocodb_project_id: Optional[str] = None
    nocodb_categories_table: Optional[str] = None
    nocodb_products_table: Optional[str] = None
    nocodb_orders_table: Optional[str] = None
    nocodb_status_table: Optional[str] = None
    nocodb_bot_commands_table: Optional[str] = None
    nocodb_options_table: Optional[str] = ""
    nocodb_options_category_table: Optional[str] = ""
    premium_expiration_date: Optional[datetime] = None
    broadcast_messages_count: Optional[int] = 0
    web_app_url: str


class ShopCategoryResponse(ShopCategory):
    id: str
