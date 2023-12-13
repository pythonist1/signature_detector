from abc import ABC, abstractmethod


class AbstractWordDetectorAdapter(ABC):
    @abstractmethod
    def detect_signatures(self, image_bytes):
        pass


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, result):
        pass
