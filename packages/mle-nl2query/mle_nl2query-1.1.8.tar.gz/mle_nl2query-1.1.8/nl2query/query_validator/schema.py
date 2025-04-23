from pydantic import BaseModel, Field
from typing import Optional


class QueryValidatorSchema(BaseModel):
    validated_query: Optional[str] = Field(..., description="")
