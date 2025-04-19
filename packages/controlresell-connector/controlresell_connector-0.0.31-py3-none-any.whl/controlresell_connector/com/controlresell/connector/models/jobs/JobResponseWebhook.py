from pydantic import BaseModel
from typing import Generic
from typing import TypeVar
from uuid import UUID

T = TypeVar('T')
class JobResponseWebhook(BaseModel, Generic[T]):
    accountId: UUID
    response: T
