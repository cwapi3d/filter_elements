import os.path
import utility_controller as uc
from language_strategy import (LanguageStrategy, EnglishLanguageStrategy, GermanLanguageStrategy,
                               FrenchLanguageStrategy, \
                               SpanishLanguageStrategy)
from message_dto import MessageDTO


class LanguageController:
    def __init__(self, strategy: LanguageStrategy):
        self._strategy = strategy

    def get_messages(self) -> MessageDTO:
        return self._strategy.get_messages()


def path_to_json_file() -> str:
    return os.path.join(uc.get_plugin_path(), 'messages.json')

def get_language_controller() -> LanguageController:
    language = uc.get_language()
    if language == 'de':
        return LanguageController(GermanLanguageStrategy(path_to_json_file()))
    elif language == 'fr':
        return LanguageController(FrenchLanguageStrategy(path_to_json_file()))
    elif language == 'es':
        return LanguageController(SpanishLanguageStrategy(path_to_json_file()))
    else:
        return LanguageController(EnglishLanguageStrategy(path_to_json_file()))
