from typing import Type
import utility_controller as uc
from language_strategy import (LanguageStrategy, EnglishLanguageStrategy, GermanLanguageStrategy,
                               FrenchLanguageStrategy, \
                               SpanishLanguageStrategy)
from message_dto import MessageDTO


class LanguageController:
    def __init__(self, strategy: Type[LanguageStrategy]):
        self._strategy = strategy()

    def get_messages(self) -> MessageDTO:
        return self._strategy.get_messages()


def get_language_controller() -> LanguageController:
    language = uc.get_language()
    if language == 'de':
        return LanguageController(GermanLanguageStrategy)
    elif language == 'fr':
        return LanguageController(FrenchLanguageStrategy)
    elif language == 'es':
        return LanguageController(SpanishLanguageStrategy)
    else:
        return LanguageController(EnglishLanguageStrategy)
