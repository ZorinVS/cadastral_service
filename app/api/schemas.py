from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from api.validators import CadastralValidator


class OrderBy(str, Enum):
    ascending = "asc"
    descending = "desc"


class QueryRequestAddDTO(BaseModel):
    cadastral_number: str = Field(..., json_schema_extra={"example": "77:01:0004012:2041"})
    latitude: float = Field(..., ge=-90, le=90, json_schema_extra={"example": 55.7558})
    longitude: float = Field(..., ge=-180, le=180, json_schema_extra={"example": 37.6173})

    @field_validator("cadastral_number", mode="before")
    def normalize_cadastral_number(cls, value: str) -> str:
        return CadastralValidator.normalize(value)

    @field_validator("cadastral_number")
    def validate_cadastral_number(cls, value: str) -> str:
        if not CadastralValidator.is_valid(value):
            raise ValueError("Incorrect cadastral number format")
        return value


class QueryResponseDTO(QueryRequestAddDTO):
    result: bool | None = Field(None)


class QueryResponsesDTO(QueryResponseDTO):
    created_at: datetime = Field(...)


class QueryHistoryResponseDTO(QueryResponsesDTO):
    id: int = Field(...)
