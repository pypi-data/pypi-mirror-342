from pydantic import BaseModel
from typing import Generic
from typing import TypeVar
from uuid import UUID
from typing import Optional

T = TypeVar('T')
class JobResponseWebhook(BaseModel, Generic[T]):
    accountId: UUID
    response: Optional[T] = None
    error: Optional[str] = None
