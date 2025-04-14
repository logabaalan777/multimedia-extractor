from pydantic import BaseModel
from typing import Union

class ExtractedTextResponse(BaseModel):
    source: str
    text: Union[dict, str]
    language: str
    timestamp: str