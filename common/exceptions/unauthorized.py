from typing import Optional
from pydantic import BaseModel, ConfigDict

class UnauthorizedError(BaseModel):
    error: str
    message: Optional[str] = None
    
    model_config = ConfigDict(use_enum_values=True)
    
class UnauthorizedException(Exception):
    def __init__(self, error: UnauthorizedError):
        super().__init__(error.message)
        self.error = error.error
        self.message = error.message
