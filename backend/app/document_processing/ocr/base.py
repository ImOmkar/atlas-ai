from abc import ABC, abstractmethod
from pathlib import Path


class BaseOCREngine(ABC):

    @abstractmethod
    def extract(
        self,
        file_path: Path,
    ) -> str:
        pass