from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobAuthLoginResponse(BaseModel):
    accountId: UUID
    error: Optional[str] = None
