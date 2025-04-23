from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrder

class JobOrdersListResponse(BaseModel):
    orders: list[JobOrder]
