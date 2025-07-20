from pydantic import BaseModel, Field


class QueryRequestDTO(BaseModel):
    cadastral_number: str = Field(..., json_schema_extra={"example": "77:01:0004012:2041"})
    latitude: float = Field(..., ge=-90, le=90, json_schema_extra={"example": 55.7558})
    longitude: float = Field(..., ge=-180, le=180, json_schema_extra={"example": 37.6173})
