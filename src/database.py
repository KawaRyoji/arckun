import abc
import json
from typing import Self


class Record:
    pass


class Query[T](metaclass=abc.ABCMeta):

    pass


class Database(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def connect(cls, endpoint: str) -> Self:
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, query):
        raise NotImplementedError()


class JSONDatabase(Database):

    def __init__(
        self,
    ) -> None:
        pass
