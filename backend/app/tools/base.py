
from abc import ABC, abstractmethod


class BaseTool(
    ABC,
):

    @abstractmethod
    def name(
        self,
    ) -> str:
        ...

    @abstractmethod
    def description(
        self,
    ) -> str:
        ...

    @abstractmethod
    def execute(
        self,
        arguments: dict,
    ):
        ...