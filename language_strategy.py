from message_dto import MessageDTO
from abc import ABC, abstractmethod
from json_reader import load_messages

MESSAGES = load_messages('messages.json')


class LanguageStrategy(ABC):
    @abstractmethod
    def get_messages(self) -> MessageDTO:
        pass


class EnglishLanguageStrategy(LanguageStrategy):
    def get_messages(self) -> MessageDTO:
        messages = MESSAGES['en']
        return MessageDTO(**messages)


class GermanLanguageStrategy(LanguageStrategy):
    def get_messages(self) -> MessageDTO:
        messages = MESSAGES['de']
        return MessageDTO(**messages)


class FrenchLanguageStrategy(LanguageStrategy):
    def get_messages(self) -> MessageDTO:
        messages = MESSAGES['fr']
        return MessageDTO(**messages)


class SpanishLanguageStrategy(LanguageStrategy):
    def get_messages(self) -> MessageDTO:
        messages = MESSAGES['es']
        return MessageDTO(**messages)
