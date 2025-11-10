from typing import List, Optional

from pydantic import BaseModel, ConfigDict

class ThreadResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class FileResponse(BaseModel):
    id: int
    name: str
    path: str
    size: int
    content_type: str


class CreateThreadResponse(BaseModel):
    thread: ThreadResponse
    success_files: List[FileResponse]
    failed_files: List[dict]
    total_files: int