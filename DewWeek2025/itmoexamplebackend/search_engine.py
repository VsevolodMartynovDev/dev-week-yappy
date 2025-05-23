from typing import Any
import uuid
from tqdm import tqdm


class SearchEngine:
    """Болванка имитирующая поисковой движок."""

    cdn_url: str = 'https://s3.ritm.media/hackaton-itmo'

    def find(self, query: str) -> list[Any]:
        """
        Типа метод вызова поиска по запросу.

        :param query: str
        :return: list[Any]
        """
        return ["/".join([self.cdn_url, str(uuid.uuid4())]) for _ in tqdm(range(10), f'Searching {query}...')]
