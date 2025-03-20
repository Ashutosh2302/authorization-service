from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class RequestedInitiatorUserHeaders(BaseModel):
    id: str
    roles: List[str]

class CredentialsType(Enum):
    JWT = "jwt"
    API_KEY = "api_key"

class CredentialsDTO(BaseModel):
    type: CredentialsType
    credential: str
    request_initiator: Optional[RequestedInitiatorUserHeaders] = None