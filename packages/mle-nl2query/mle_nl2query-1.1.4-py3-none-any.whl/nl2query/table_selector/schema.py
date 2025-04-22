from pydantic import BaseModel, Field
from typing import List, Optional


class TableSelectorSchema(BaseModel):
    selected_tables: Optional[List] = Field(
        ..., description="List of tables realted to given user query."
    )
