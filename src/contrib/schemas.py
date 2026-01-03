from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import UUID4, BaseModel, Field, field_serializer


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True


class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Data de criação")]

    @field_serializer("created_at")
    def serialize_dt(self, dt: datetime, _info):
        br_time = dt.astimezone(ZoneInfo("America/Sao_Paulo"))
        return br_time.isoformat()
