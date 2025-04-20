from pydantic import BaseModel
from typing import Optional

class UpdateAccountPayload(BaseModel):
    credentials: Optional[str] = None
    data: Optional[str] = None
