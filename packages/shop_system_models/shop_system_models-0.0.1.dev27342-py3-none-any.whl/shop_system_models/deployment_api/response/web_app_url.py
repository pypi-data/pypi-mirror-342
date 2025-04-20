from pydantic import BaseModel


class WebAppUrlResponse(BaseModel):
    web_app_url: str