import jwt
import os

from models.endpoints.authorize_request import AuthorizeRequestUnauthorizedErrorEnum, raise_unauthorized_error, raise_forbidden_error, UserDetails, AuthorizeRequestDTO
from models.common.credentials import CredentialsDTO, CredentialsType
from dotenv import load_dotenv  
from persistence.dao.api_key_dao import ApiKeyDao
from persistence.api_key_persistence import ApiKeyPersistence
from typing import Optional
load_dotenv()

class AuthorizationService:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        
    # def __check_access(self, roles: list[str], method_endpoint: str) -> bool:
    #     has_access = self.endpoint_service.have_access_to_endpoint(roles, method_endpoint)
    #     if not has_access:
    #         raise_forbidden_error(AuthorizeRequestForbiddenErrorEnum.ACCESS_DENIED)

    def __get_api_key(self, credential: str) -> ApiKeyDao:
        api_key_dao: Optional[ApiKeyDao] = ApiKeyPersistence().get(credential)
        if not api_key_dao:
            raise_unauthorized_error(AuthorizeRequestUnauthorizedErrorEnum.API_KEY_NOT_FOUND)
        return api_key_dao

    def __decode_token(self, token: str) -> UserDetails:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            role_ids = payload.get('roles', [])
            user_id = payload.get('id')
            college_id = payload.get('college_id')
            return UserDetails(id=user_id, roles=role_ids, college_id=college_id)
        except jwt.ExpiredSignatureError:
            raise_unauthorized_error(AuthorizeRequestUnauthorizedErrorEnum.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise_unauthorized_error(AuthorizeRequestUnauthorizedErrorEnum.INVALID_TOKEN)

    def __authorize_token(self, token: str) -> UserDetails:
        user_details = self.__decode_token(token)

        print("user_details::", user_details)

        if user_details.id is None:
            raise_unauthorized_error(AuthorizeRequestUnauthorizedErrorEnum.INVALID_TOKEN)   
        # if not user_details.roles:
        #     raise_forbidden_error(AuthorizeRequestUnauthorizedErrorEnum.INVALID_TOKEN)

        return user_details
    
    
    def __authorize_api_key(self, credential: CredentialsDTO, method_endpoint: str) -> UserDetails:
        api_key_dao: ApiKeyDao = self.__get_api_key(credential.credential)

        # self.__check_access(api_key_dao.roles, method_endpoint)

        if credential.request_initiator:
            # self.__check_access(credential.request_initiator.roles, method_endpoint)
            return UserDetails(id=credential.request_initiator.id, roles=credential.request_initiator.roles, system_carrier=True)
        
        return UserDetails(api_key_id=api_key_dao.id, roles=api_key_dao.roles, system_carrier=True)

    def authorize_request(self, credential: CredentialsDTO, request: AuthorizeRequestDTO) -> UserDetails:
        if credential.type == CredentialsType.API_KEY:
            return self.__authorize_api_key(credential, request.method_endpoint)
        else:
            return self.__authorize_token(credential.credential, request.method_endpoint)
        