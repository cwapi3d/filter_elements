#!/usr/bin/env python

"""filter_elements.py: searches elements for specific terms and activates them """

__author__ = "Michael Brunner"
__copyright__ = "Copyright 2022, Cadwork Holz AG"
__maintainer__ = "Michael Brunner"
__email__ = "brunner@cadwork.swiss"
__license__ = "MIT License Agreement"
__version__ = "1.0"
__status__ = "Release"

import dataclasses
import os
import sys
from typing import List
import logging
import utility_controller as uc
import element_controller as ec
import attribute_controller as ac
import re
import visualization_controller as vc
import tkinter
import tkinter.messagebox
from collections import defaultdict


os.environ['PYTHONPATH'] = os.pathsep.join([
    os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages'),
    os.path.join(os.path.dirname(__file__), 'src'),
    os.path.dirname(__file__),
    os.path.join(uc.get_plugin_path()),
])

sys.path.extend(os.environ['PYTHONPATH'].split(os.pathsep))

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("{asctime} {levelname}: {message}", "%d.%m.%Y %H:%M:%S", style="{")
handler.setFormatter(formatter)
logger = logging.getLogger(__file__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main(message):
    element_ids = query_elements_to_filter(message)

    if list_is_empty(element_ids):
        return

    set_elements_state_inactive_and_refresh_display(element_ids)
    uc.disable_auto_display_refresh()

    names = get_element_names(element_ids)

    elements = list()

    find_word = uc.get_user_string(message[2])
    if find_word == '':
        return

    search = re.split(', |;|,|\s', find_word)
    search = list(map(str.lower, search))

    elements_to_filter = FilterElements(element_ids).element_records
    word_splitting_pattern = ', |;|,|\s'
    name_filter = NameFilter(word_splitting_pattern, find_word, elements_to_filter)
    results = name_filter.matching_results()

    for n, e in zip(names, element_ids):
        if any(x in n for x in search):
            elements.append(e)
        else:
            continue

    if not elements:
        warning_msg(message[3])

    uc.enable_auto_display_refresh()
    activate_matching_elements(elements)
    info_msg(f"{len(elements)} {message[4]} ")

    return None


def query_elements_to_filter(message):
    active_element_ids = ec.get_active_identifiable_element_ids()
    visible_element_ids = ec.get_visible_identifiable_element_ids()
    if (list_is_empty(active_element_ids) and
            not list_length_identical(active_element_ids, visible_element_ids)):
        element_ids = get_elements_by_user_decision(active_element_ids, message, visible_element_ids)
    else:
        element_ids = visible_element_ids
    return element_ids


def activate_matching_elements(elements):
    vc.set_active(elements)


def get_element_names(element_ids: List[int]):
    return list(map(get_name, element_ids))


def set_elements_state_inactive_and_refresh_display(element_ids: List[int]):
    if not list_is_empty(element_ids):
        vc.set_inactive(element_ids)


def get_elements_by_user_decision(active_element_ids: List[int], message, visible_element_ids: List[int]):
    var: bool = uc.get_user_bool(message[1], True)
    element_ids = active_element_ids if var else visible_element_ids
    return element_ids


def strings_to_lower(strings: List[str]):
    return list(map(lambda string: string.lower(), strings))


def list_is_empty(element_list: List[int]):
    return len(element_list) == 0


def list_length_identical(fst_element_list: List[int], snd_element_list: List[int]):
    return len(fst_element_list) == len(snd_element_list)


@dataclasses.dataclass
class ElementRecord:
    element_id: int
    name: str


class FilterElements:
    def __init__(self, elements: List[int]):
        if len(elements) == 0:
            raise Exception("Size elements must not be null")

        self._element_records: List[ElementRecord] = self._create_records(elements)

    @staticmethod
    def _create_records(elements: List[int]) -> List[ElementRecord]:
        return list(
            map(lambda element_id: ElementRecord(element_id, ac.get_name(element_id)), elements))

    @property
    def element_records(self) -> List[ElementRecord]:
        return self._element_records


class NameFilter:
    def __init__(self, pattern, words_to_find: str, elements: List[ElementRecord]):
        if len(pattern) == 0:
            raise Exception("Pattern must not be empty")
        if len(words_to_find) == 0:
            raise Exception("Text sequence for searching must not be empty")
        if len(elements) == 0:
            raise Exception("Size elements must not be null")
        self.pattern = pattern
        self.words_to_find = self._split_words_to_find_by_pattern(words_to_find)
        self.elements = elements

    def matching_results(self) -> List[int]:
        return [element.element_id for element in self.elements
                if (any(term in element.name for term in self.words_to_find))]

    def _split_words_to_find_by_pattern(self, words_to_find):
        return re.split(self.pattern, words_to_find)


# ---------------------------------------------------------------
def get_message_lang():
    # language dictionary
    language_dict = defaultdict(list)
    language_dict['en'] = ['No elements are active/visible!', 'Should only active elements be considered?',
                           'Enter search term', 'Names not found', ' Elements found']
    language_dict['de'] = ['Es sind keine Elemente aktiv/sichtbar!',
                           'Sollen nur aktive Elemente berücksichtigt werden?', 'Suchbegriff eingeben',
                           'Namen nicht gefunden!', ' Elemente gefunden']
    language_dict['fr'] = ["Aucun élément n'est actif/visible !",
                           'Seuls les éléments actifs doivent-ils être pris en compte ?', 'Saisir un mot-clé',
                           'Noms non trouvés', ' Éléments trouvés']
    language_dict['es'] = ['¡No hay elementos activos/visibles!', '¿Sólo se deben considerar los elementos activos?',
                           'Introduzca el término de búsqueda', 'Nombres no encontrados', ' Elementos encontrados']

    language = uc.get_language()
    if language == 'de':
        return language_dict['de']
    elif language == 'fr':
        return language_dict['fr']
    elif language == 'es':
        return language_dict['es']
    else:
        return language_dict['en']


def warning_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title="Achtung", message=message)
    root.destroy()


def info_msg(message):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title="Information", message=message)
    root.destroy()


def get_name(element: int) -> str:
    name = ac.get_name(element)
    return name.lower()


if __name__ == '__main__':
    init_and_setup_logger()

    main(message=get_message_lang())
