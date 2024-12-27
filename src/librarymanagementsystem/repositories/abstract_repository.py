from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def read_all(self, filter_type: str = None, filter_text: str = None):
        pass

    @abstractmethod
    def insert(self, entity):
        pass

    @abstractmethod
    def modify(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass
