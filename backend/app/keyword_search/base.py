from abc import ABC, abstractmethod


class BaseKeywordSearchProvider(
    ABC,
):

    @abstractmethod
    def search(
        self,
        organization_id: int,
        project_id: int,
        query: str,
        limit: int = 10,
    ):
        ...