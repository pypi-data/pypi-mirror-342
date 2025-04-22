from typing import Literal

from .._models import BaseModel

__all__ = ["AlmanakUser", "AlmanakUserTeam"]


class AlmanakUser(BaseModel):
    id: str
    """The user identifier, which can be referenced in the API endpoints."""

    name: str
    """The Unix timestamp (in seconds) when the model was created."""

    email: str
    """The email of the user, used to login into the account"""

    notification_email: str
    """The email used to notify the user"""


class AlmanakUserTeam(BaseModel):
    organisation_id: str
    """The organisation identifier, which can be referenced in the API endpoints."""

    team_id: str
    """The team identifier, which can be referenced in the API endpoints."""

    role: Literal["ADMIN", "MEMBER"]
    """The role of the user in the team"""

    user: AlmanakUser
    """The user object containing the user information"""
