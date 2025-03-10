from pydantic import BaseModel, model_validator
from enum import  Enum
from common.exceptions.unauthorized import UnauthorizedError, UnauthorizedException
from common.exceptions.forbidden import ForbiddenError, ForbiddenException
from typing import Union, Optional


class UserDetails(BaseModel):
    id: Optional[str] = None
    college_id: Optional[str] = None
    api_key_id: Optional[str] = None
    roles: list[str]
    system_carrier: bool = False

    @model_validator(mode="before")
    @classmethod
    def check_id_or_api_key_id(cls, v):
        if v.get("id", None) is None and v.get("api_key_id", None) is None:
            raise ValueError("Either id or api_key_id must be present")
        return v

class AuthorizeRequestDTO(BaseModel):
    pass

class AuthorizeRequestUnauthorizedErrorEnum(Enum):
    EXPIRED_TOKEN = "expired_token"
    INVALID_TOKEN = "invalid_token"
    INVALID_API_KEY = "invalid_api_key"
    NO_TOKEN_OR_API_KEY_PROVIDED = "no_token_or_api_key_provided"
    API_KEY_NOT_FOUND = "api_key_not_found"
   

class AuthorizeRequestUnauthorizedErrorMessages(Enum):
    EXPIRED_TOKEN = "Token has expired"
    INVALID_TOKEN = "Invalid token"
    INVALID_API_KEY = "Invalid API key"     
    NO_TOKEN_OR_API_KEY_PROVIDED = "No token or API key provided"
    API_KEY_NOT_FOUND = "API key not found"


class AuthorizeRequestUnauthorizedError(UnauthorizedError):
    error: AuthorizeRequestUnauthorizedErrorEnum
    message: Union[AuthorizeRequestUnauthorizedErrorMessages, str]

    @model_validator(mode="before")
    @classmethod
    def set_error_message(cls, v):
        error = AuthorizeRequestUnauthorizedErrorEnum(v["error"]).name
        if v.get("message", None) is None:
            v["message"] = AuthorizeRequestUnauthorizedErrorMessages[error].value 
        return v


def raise_unauthorized_error(error: AuthorizeRequestUnauthorizedErrorEnum , message: Optional[Union[AuthorizeRequestUnauthorizedErrorMessages, str]] = None):
    raise UnauthorizedException(
            AuthorizeRequestUnauthorizedError(
                error=error,
                message=message
            )
        )


class AuthorizeRequestForbiddenErrorEnum(Enum):
    ACCESS_DENIED = "access_denied"

class AuthorizeRequestForbiddenErrorMessages(Enum):
    ACCESS_DENIED = "Insufficient permissions"

class AuthorizeRequestForbiddenError(ForbiddenError):
    error: AuthorizeRequestForbiddenErrorEnum
    message: Union[AuthorizeRequestForbiddenErrorMessages, str]

    @model_validator(mode="before")
    @classmethod
    def set_error_message(cls, v):
        error = AuthorizeRequestForbiddenErrorEnum(v["error"]).name
        if v.get("message", None) is None:
            v["message"] = AuthorizeRequestForbiddenErrorMessages[error].value
        return v

def raise_forbidden_error(error: AuthorizeRequestForbiddenErrorEnum, message: Optional[Union[AuthorizeRequestForbiddenErrorMessages, str]] = None):
    raise ForbiddenException(
            AuthorizeRequestForbiddenError(
                error=error,
                message=message
            )
        )
