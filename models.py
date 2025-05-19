from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(None, description="Auto-generated UUID")
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., example=25, gt=0, lt=150, description="Возраст должен быть положительным числом")