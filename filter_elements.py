#!/usr/bin/env python

"""filter_elements.py: searches elements for specific terms and activates them """

__author__ = "Michael Brunner"
__copyright__ = "Copyright 2022, Cadwork Holz AG"
__maintainer__ = "Michael Brunner"
__email__ = "brunner@cadwork.swiss"
__license__ = "MIT License Agreement"
__version__ = "1.0"
__status__ = "Release"

import logging
import os
import sys
from collections import defaultdict
from typing import List, Type

import attribute_controller as ac
import element_controller as ec
import utility_controller as uc
import visualization_controller as vc

from message_dto import MessageDTO

os.environ['PYTHONPATH'] = os.pathsep.join([
    os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages'),
    # os.path.dirname(__file__),
    os.path.join(uc.get_plugin_path()),
])

sys.path.extend(os.environ['PYTHONPATH'].split(os.pathsep))

from FilterElements import FilterElements
from language_controller import LanguageController, get_language_controller
from NameFilter import NameFilter

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("{asctime} {levelname}: {message}", "%d.%m.%Y %H:%M:%S", style="{")
handler.setFormatter(formatter)
logger = logging.getLogger(__file__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class FilterElementController:
    def __init__(self, language_controller: LanguageController):
        self._language_controller = language_controller

    def find_matching_element_names_by_user_query(self) -> List[int]:
        pass

    def activate_resulting_elements(self):
        pass


def find_matching_element_names_by_user_query(message: MessageDTO):
    element_ids = query_elements_to_filter(message)

    if list_is_empty(element_ids):
        return

    set_elements_state_inactive_and_refresh_display(element_ids)
    uc.disable_auto_display_refresh()

    try:
        query = query_filter_text_fragments(message)
    except RuntimeError:
        logger.error("no text was entered in user query")
        return

    elements_to_filter = FilterElements(element_ids).element_records

    word_splitting_pattern = ', |;|,|\s'
    name_filter = NameFilter(word_splitting_pattern, query, elements_to_filter)
    results = name_filter.matching_results()

    uc.enable_auto_display_refresh()
    activate_matching_elements(results)

    return


def query_filter_text_fragments(message):
    find_word = uc.get_user_string(message[2])
    if len(find_word) == 0:
        raise RuntimeError("Query must not be empty")

    return find_word


def query_elements_to_filter(message):
    active_element_ids = ec.get_active_identifiable_element_ids()
    visible_element_ids = ec.get_visible_identifiable_element_ids()
    if (not list_is_empty(active_element_ids) and
            not list_length_identical(active_element_ids, visible_element_ids)):
        logger.info(
            f"{len(active_element_ids)} of {len(visible_element_ids)} elements state is active")
        element_ids = get_elements_by_user_decision(active_element_ids, message, visible_element_ids)
    else:
        logger.info(f"{len(visible_element_ids)} are visible")
        element_ids = visible_element_ids
    return element_ids


def activate_matching_elements(elements):
    vc.set_active(elements)


def get_element_names(element_ids: List[int]):
    return list(map(get_name, element_ids))


def set_elements_state_inactive_and_refresh_display(element_ids: List[int]):
    if not list_is_empty(element_ids):
        logger.info(f"{len(element_ids)} elements state changed to inactive")
        vc.set_inactive(element_ids)


def get_elements_by_user_decision(active_element_ids: List[int], message, visible_element_ids: List[int]):
    var = uc.get_user_bool(message[1], True)
    element_ids = active_element_ids if var else visible_element_ids
    return element_ids


def strings_to_lower(strings: List[str]):
    return list(map(lambda string: string.lower(), strings))


def list_is_empty(element_list: List[int]):
    return len(element_list) == 0


def list_length_identical(fst_element_list: List[int], snd_element_list: List[int]):
    return len(fst_element_list) == len(snd_element_list)


# ---------------------------------------------------------------
def get_messages_based_on_user_language() -> MessageDTO:
    language_controller = get_language_controller()
    return language_controller.get_messages()


def get_name(element: int) -> str:
    name = ac.get_name(element)
    return name.lower()


if __name__ == '__main__':
    find_matching_element_names_by_user_query(get_messages_based_on_user_language())
