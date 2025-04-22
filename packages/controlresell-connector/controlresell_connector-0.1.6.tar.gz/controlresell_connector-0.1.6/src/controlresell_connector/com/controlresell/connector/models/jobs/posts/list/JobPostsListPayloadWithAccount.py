from pydantic import BaseModel
from uuid import UUID

class JobPostsListPayloadWithAccount(BaseModel):
    accountId: UUID
