from pydantic import BaseModel
from typing import Optional

class JobAuthDataResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
