from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class IssueRequest(BaseModel):
    url: HttpUrl
    purpose: str = Field(examples=["parking-payment", "museum-ticket", "donation"])
    ttl_seconds: Optional[int] = None

class IssueResponse(BaseModel):
    token: str  # compact JWS
    expires_at: int
