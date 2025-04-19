from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListed

class JobPostsListResponse(BaseModel):
    posts: list[JobPostListed]
