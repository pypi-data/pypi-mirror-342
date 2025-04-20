from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import Field, field_validator, BaseModel

from shop_system_models.shop_api.shop.response.baskets import UserBasketResponseModelV2
from pydantic_core.core_schema import ValidationInfo
from shop_system_models.consts.country_codes import ISO3166



class ExtraFieldPayload(BaseModel):
    name: str
    value: str


class OrderDeliveryTypeModel(BaseModel):
    name: str
    address: str | None = ""
    amount: float | None = 0.0
    extra_fields_payload: list[ExtraFieldPayload] | None = []


class Coordinates(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


class AddressModel(BaseModel):
    coordinates: Coordinates | None = None
    address: str | None = None


class ExtraField(BaseModel):
    name: str
    description: str
    is_required: bool | None


class DeliveryTypeModel(BaseModel):
    name: str
    amount: float = 0.0
    is_address_required: bool | None = False
    address_hint: str | None = ""
    extra_fields: list[ExtraField] = []
    is_timepicker_required: bool = False
    details: str | None = ""
    country: str | None = ""
    country_code: str | None = ""  # ISO format, ex.: RU, KZ, BY...
    city: str | None = ""
    delivery_location: Coordinates | None = None
    delivery_radius: int | None = None
    delivery_min_hour: int | None = None
    delivery_max_hour: int | None = None
    delivery_minutes_interval: int | None = None
    delivery_min_day: int | None = None
    delivery_max_day: int | None = None

    @field_validator("country_code", mode="before")
    def set_country_code(cls, value, values: ValidationInfo):
        country_code_upper = value.upper()
        if ISO3166.get(country_code_upper):
            return country_code_upper
        return "RU"


def format_order_number(order_count: int) -> str:
    return f"#{order_count:04}"


"""
{
    "user_id": 123,
    "basket_id": None,
    "basket": None,
    "status": "booking_request",
    "delivery": None,
    "delivery_date_from": None,
    "user_contact_number": None,
    "client_coordinates": None,
    "comment": "",# НАДО
    "payment_type_id": # НАДО
    "preview_url": ''
    "booking_details": {
        "booking_id": "123123",
        "from_date": datetime.now(),
        "till_date": datetime.now(),
        "item_id": "123123",
    }
}"""


class BookingOrderModel(BaseModel):
    booking_id: str
    from_date: datetime
    till_date: datetime
    item_id: str


class CreateOrderModel(BaseModel):
    delivery: OrderDeliveryTypeModel | None = None
    delivery_date_from: datetime = Field(default_factory=datetime.now)
    comment: str | None = None
    user_contact_number: str | None = None
    payment_type_id: str | None = None
    booking_details: BookingOrderModel | None = None
    preview_url: str | None = ""


class OrderPaymentDetails(BaseModel):
    title: str
    description: str
    expires_at: datetime
    link: str


class OrderModel(CreateOrderModel):
    basket: UserBasketResponseModelV2
    user_id: str | None = None
    basket_id: str | None = None
    status: str | None = None
    client_coordinates: AddressModel | None = None
    created: datetime = datetime.now()
    updated: datetime = datetime.now()
    order_number: str = "#0001"
    process_key: int | None = None
    coupon: str | None = None
    admin_message_id: str | None = None

    payment_data: OrderPaymentDetails | None = None


class LabeledPrice(BaseModel):
    label: str
    amount: int


class InvoiceBaseModel(BaseModel):
    chat_id: int
    order_id: str
    order_number: str  # order_number
    payload: str  # <basket_id>_<order_id>_<order_number> from OrderResponseModel --> its subscription key
    amount: float
    currency: str  # fiat
    payment_address: str
    payment_timeout: int | None = None


class InvoiceTGMessageModel(InvoiceBaseModel):
    description: str  # order_products
    provider_data: str | None = None
    prices: list[LabeledPrice]  # label and amount in coins!
    need_name: bool | None = False
    need_phone_number: bool | None = False
    need_email: bool | None = False
    send_phone_number_to_provider: bool | None = False
    send_email_to_provider: bool | None = False
    is_flexible: bool | None = False
    reply_markup: bool | None = None


class InvoiceWithPaymentLinkMessageModel(InvoiceBaseModel):
    payment_link: str


class InvoiceTONMessageModel(InvoiceBaseModel):
    approved_addresses: list[str] = []
    ton_amount: float


class PaidContentMessage(BaseModel):
    message: str
