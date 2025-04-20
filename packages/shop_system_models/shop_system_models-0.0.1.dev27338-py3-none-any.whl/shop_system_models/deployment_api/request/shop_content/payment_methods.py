from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class PaymentTypes(str, Enum):
    manual_payment_request = 'ManualPaymentRequest'
    external_card_payment_provider = 'ExternalCardPaymentProvider'
    crypto_ton = 'CryptoTON'
    xtr = 'XTR'
    life_pay = 'LifePay'
    yookassa = "yookassa"
    tkassa = "tkassa"

class Metadata(BaseModel):
    key: str
    value: List[str]


class PaymentMethod(BaseModel):
    name: str
    type: PaymentTypes
    payment_data: str  # payment_token, TON address etc....
    meta: Optional[List[Metadata]] = []

    class Config:
        use_enum_values = True


class PaymentMethodResponse(PaymentMethod):
    id: str
