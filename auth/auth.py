from fastapi import Request, Depends, Header
from service.authorization_service import AuthorizationService
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from typing import Optional
from models.endpoints.authorize_request import UserDetails, AuthorizeRequestUnauthorizedErrorEnum, raise_unauthorized_error
from models.common.credentials import CredentialsDTO, CredentialsType, RequestedInitiatorUserHeaders
from models.endpoints.authorize_request import AuthorizeRequestDTO

authorization_service = AuthorizationService()  

def jwt_auth(
    token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
):
    if not token:
        return None
    return CredentialsDTO(type=CredentialsType.JWT, credential=token.credentials)


def request_initiator_user_info(
    id: Optional[str] = Header(alias="X-Requested-By-User-Id", default=None),
    roles: Optional[str] = Header(alias="X-Requested-By-User-Roles", default=None),
) -> Optional[RequestedInitiatorUserHeaders]:
    if not id or not roles:
        return None
    return RequestedInitiatorUserHeaders(id=id, roles=roles)


def api_key_auth(api_key=Depends(APIKeyHeader(name="X-API-Key", auto_error=False))) -> Optional[CredentialsDTO]:
    if not api_key:
        return None
    return CredentialsDTO(type=CredentialsType.API_KEY, credential=api_key)


async def credentials(
    jwt: Optional[CredentialsDTO] = Depends(jwt_auth),
    user_headers: Optional[RequestedInitiatorUserHeaders] = Depends(request_initiator_user_info),
    api_key: Optional[CredentialsDTO] = Depends(api_key_auth),
) -> CredentialsDTO:
    if not api_key and not jwt:
        raise_unauthorized_error(AuthorizeRequestUnauthorizedErrorEnum.NO_TOKEN_OR_API_KEY_PROVIDED)
    credential = api_key if api_key is not None else jwt
    assert credential is not None
    return CredentialsDTO(type=credential.type, credential=credential.credential, request_initiator=user_headers)


def authorizer(request: Request, credential: CredentialsDTO = Depends(credentials)) -> UserDetails:
    endpoint = request.url.path
    method = request.method.upper()
    return ping_authorization_service(credential, f"{method}__{endpoint}")


def ping_authorization_service(credentials: CredentialsDTO, method_endpoint: str) -> UserDetails:
    return authorization_service.authorize_request(credentials, AuthorizeRequestDTO(method_endpoint=method_endpoint))                             
