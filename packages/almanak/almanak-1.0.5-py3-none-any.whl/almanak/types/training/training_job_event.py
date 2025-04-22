from typing import Literal

from ..._models import BaseModel

__all__ = ["TrainingJobEvent"]


class TrainingJobEvent(BaseModel):
    id: str

    created_at: int

    level: Literal["info", "warn", "error"]

    message: str

    object: Literal["training.job.event"]
