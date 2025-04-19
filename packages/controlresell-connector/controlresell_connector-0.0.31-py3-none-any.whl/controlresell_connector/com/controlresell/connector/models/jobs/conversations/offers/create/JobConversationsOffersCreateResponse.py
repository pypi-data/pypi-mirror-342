from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.conversations.offers.JobConversationOffer import JobConversationOffer

class JobConversationsOffersCreateResponse(BaseModel):
    offer: JobConversationOffer
