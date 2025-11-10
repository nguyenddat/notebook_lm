from typing import List, Dict, Any

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class Citation(BaseModel):
    source_text: str = Field(..., description="Văn bản trích dẫn cụ thể từ tài liệu, được dùng để hỗ trợ câu trả lời.")
    page_number: int = Field(..., description="Vị trí số trang của nguồn trích dẫn trong file.")
    filename: str = Field(..., description="Tên file gốc của nguồn trích dẫn.")


class RagResponse(BaseModel):
    response: str = Field(..., description="Câu trả lời khoa học, khách quan cho câu hỏi người dùng. BẮT BUỘC phải chứa các trích dẫn trong ngoặc vuông theo phong cách IEEE (ví dụ: [1], [2]).")
    
    citations: List[Dict[str, Any]] = Field(..., description="Danh sách các nguồn tài liệu chi tiết được tham chiếu trong câu trả lời. Mỗi nguồn có định dạng như sau: {{source_text: str, page_number: int, filename: str}}.")

parser = PydanticOutputParser(pydantic_object=RagResponse)