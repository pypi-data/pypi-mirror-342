from pydantic import BaseModel, Field
from typing import Dict, Optional


class QueryReframerSchema(BaseModel):
    reframed_query: Optional[str] = Field(
        ..., description="Reframed natural language query with detailed information."
    )


class QueryReframerConfigSchema(BaseModel):
    """Schema for the key point."""

    mapping_output: Optional[Dict] = Field(
        ..., description="Config mapping of technical terms to datatbase schema."
    )
