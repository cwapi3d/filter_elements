from typing import List
import attribute_controller as ac

from ElementRecordDTO import ElementRecordDTO


class FilterElements:
    def __init__(self, elements: List[int]):
        if len(elements) == 0:
            raise RuntimeError("Size elements must not be null")

        self._element_records: List[ElementRecordDTO] = self._create_records(elements)

    @staticmethod
    def _create_records(elements: List[int]) -> List[ElementRecordDTO]:
        return list(
            map(lambda element_id: ElementRecordDTO(element_id, ac.get_name(element_id)), elements))

    @property
    def element_records(self) -> List[ElementRecordDTO]:
        return self._element_records
