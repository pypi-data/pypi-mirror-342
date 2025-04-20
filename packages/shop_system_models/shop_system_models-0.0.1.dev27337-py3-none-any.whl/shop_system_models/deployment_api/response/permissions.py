from pydantic import BaseModel


class InviteLinkResponse(BaseModel):
    valid_until: int
    link: str