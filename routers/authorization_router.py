from fastapi import APIRouter, Depends

from service.authorization_service import AuthorizationService
from models.endpoints.authorize_request import AuthorizeRequestUnauthorizedError, AuthorizeRequestForbiddenError, UserDetails, AuthorizeRequestDTO
from auth.auth import credentials
from models.common.credentials import CredentialsDTO

authorization_router = APIRouter()
authorization_service = AuthorizationService()   

@authorization_router.post('', status_code=200, responses={ 401: {"model": AuthorizeRequestUnauthorizedError}, 403: {"model": AuthorizeRequestForbiddenError}})
def authorize_request(credential: CredentialsDTO = Depends(credentials)) -> UserDetails:
    return authorization_service.authorize_request(credential)
