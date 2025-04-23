from typing import List
from pydantic import BaseModel

class ToolFilter(BaseModel):
    app_id: str | None = None
    category_id: str | None = None
    tool_ids: List[str] | None
