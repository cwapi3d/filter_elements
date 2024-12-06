import re
from typing import List

from element_dto import ElementRecordDTO


def strings_to_lower(strings: List[str]):
    return list(map(lambda string: string.lower(), strings))


class NameFilter:
    def __init__(self, pattern, words_to_find: str, elements: List[ElementRecordDTO]):
        if len(pattern) == 0:
            raise RuntimeError("Pattern must not be empty")
        if len(words_to_find) == 0:
            raise RuntimeError("Text sequence for searching must not be empty")
        if len(elements) == 0:
            raise RuntimeError("Size elements must not be null")
        self.pattern = pattern
        split_words = self._split_words_to_find_by_pattern(words_to_find)
        self.words_to_find = strings_to_lower(split_words)
        self.elements = elements

    def matching_results(self) -> List[int]:
        return [element.element_id for element in self.elements
                if (any(term in element.name.lower() for term in self.words_to_find))]

    def _split_words_to_find_by_pattern(self, words_to_find):
        return re.split(self.pattern, words_to_find)
