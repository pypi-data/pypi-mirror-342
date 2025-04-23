from typing import List
from pydantic import BaseModel

class ToolSummary(BaseModel):
    tool_id: str | None
    entities: List[str] | None
    operation: str | None
    title: str | None
    description: str | None
    is_unified_tool: bool | None
