from typing import List, Optional, Type

from mongoengine import Document, QuerySet
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned


class BasePersistence:
    @classmethod
    def get_first(cls, id: str, dao_cls: Type[Document]) -> Document:
        dao: Document = dao_cls.objects(id=id).first()
        return dao

    @classmethod
    def query(
        cls, query: dict, dao_cls: Type[Document], start: int = 0, limit: int = 10
    ) -> List[Document]:
        q_set: QuerySet = dao_cls.objects[start : start + limit]
        daos: List[Document] = list(q_set.filter(**query))
        return daos

    @classmethod
    def find_one(cls, query: dict, dao_cls: Type[Document]) -> Optional[Document]:
        try:
            q_set: QuerySet = dao_cls.objects
            dao: Document = q_set.get(**query)
        except MultipleObjectsReturned:
            raise ValueError("Multiple objects returned for query")
        except DoesNotExist:
            return None

        return dao

    @classmethod
    def save(cls, dao: Document) -> Document:
        dao.save()
        return dao
    