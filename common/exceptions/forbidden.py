from typing import Optional
from pydantic import BaseModel, ConfigDict

class ForbiddenError(BaseModel):
    error: str
    message: Optional[str] = None
    
    model_config = ConfigDict(use_enum_values=True)
    
class ForbiddenException(Exception):
    def __init__(self, error: ForbiddenError):
        super().__init__(error.message)
        self.error = error.error
        self.message = error.message
