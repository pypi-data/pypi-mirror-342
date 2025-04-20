from pydantic import BaseModel
from typing import Optional

class JobPostsListPayload(BaseModel):
    lastRetrieve: Optional[str] = None
