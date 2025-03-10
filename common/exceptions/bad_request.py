from typing import Optional

from pydantic import BaseModel, ConfigDict


class BadRequestError(BaseModel):
    error: str
    message: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class BadRequestException(Exception):
    def __init__(self, error: BadRequestError):
        super().__init__(error.message)
        self.error = error.error
        self.message = error.message