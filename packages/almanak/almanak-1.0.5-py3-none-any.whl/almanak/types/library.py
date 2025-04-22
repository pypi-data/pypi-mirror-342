from .._models import BaseModel


class FileDeleted(BaseModel):
    affected_rows: int
