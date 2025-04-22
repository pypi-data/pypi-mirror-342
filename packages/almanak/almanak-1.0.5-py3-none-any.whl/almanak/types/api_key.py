from .._models import BaseModel

__all__ = [
    "ApiKey",
]


class ApiKey(BaseModel):
    user_id: str
    created_at: str
    api_key: str
    active: bool
