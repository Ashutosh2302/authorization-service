from persistence.dao.api_key_dao import ApiKeyDao
from typing import Optional

class ApiKeyPersistence():
    def get(self, api_key:str) -> Optional[ApiKeyDao]:
        return ApiKeyDao.objects(api_key=api_key).first()
