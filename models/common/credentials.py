from enum import Enum
from pydantic import BaseModel
from typing import Optional


class RequestedInitiatorUserHeaders(BaseModel):
    id: str
    roles: str

class CredentialsType(Enum):
    JWT = "jwt"
    API_KEY = "api_key"

class CredentialsDTO(BaseModel):
    type: CredentialsType
    credential: str
    request_initiator: Optional[RequestedInitiatorUserHeaders] = None