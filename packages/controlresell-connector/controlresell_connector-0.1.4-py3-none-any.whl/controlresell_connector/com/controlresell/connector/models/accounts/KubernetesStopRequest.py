from pydantic import BaseModel
from uuid import UUID

class KubernetesStopRequest(BaseModel):
    accountId: UUID
    check: int
