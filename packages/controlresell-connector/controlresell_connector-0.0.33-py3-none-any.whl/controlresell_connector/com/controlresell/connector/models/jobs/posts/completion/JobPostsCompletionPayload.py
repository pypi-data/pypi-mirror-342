from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPost import JobPost

class JobPostsCompletionPayload(BaseModel):
    accountId: UUID
    platformId: str
    post: JobPost
