from pydantic import BaseModel, Field
from typing import Dict, Optional


class IntentJsonSchema(BaseModel):
    """Schema for the key points extracted from the transcript."""

    intent_json: Optional[Dict] = Field(..., description="")
