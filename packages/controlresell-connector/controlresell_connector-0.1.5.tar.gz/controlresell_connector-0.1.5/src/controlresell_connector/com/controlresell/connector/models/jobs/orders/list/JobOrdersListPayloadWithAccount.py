from pydantic import BaseModel
from uuid import UUID

class JobOrdersListPayloadWithAccount(BaseModel):
    accountId: UUID
