from message_dto import MessageDTO
from abc import ABC, abstractmethod
from json_reader import load_messages


class LanguageStrategy(ABC):
    def __init__(self, json_file: str):
        self._messages = load_messages(json_file)

    @property
    def messages(self):
        return self._messages

    @abstractmethod
    def get_messages(self) -> MessageDTO:
        pass


class EnglishLanguageStrategy(LanguageStrategy):

    def __init__(self, json_file: str):
        super().__init__(json_file)

    def get_messages(self) -> MessageDTO:
        messages = self.messages['en']
        return MessageDTO(**messages)


class GermanLanguageStrategy(LanguageStrategy):

    def __init__(self, json_file: str):
        super().__init__(json_file)

    def get_messages(self) -> MessageDTO:
        messages = self.messages['de']
        return MessageDTO(**messages)


class FrenchLanguageStrategy(LanguageStrategy):

    def __init__(self, json_file: str):
        super().__init__(json_file)

    def get_messages(self) -> MessageDTO:
        messages = self.messages['fr']
        return MessageDTO(**messages)


class SpanishLanguageStrategy(LanguageStrategy):

    def __init__(self, json_file: str):
        super().__init__(json_file)

    def get_messages(self) -> MessageDTO:
        messages = self.messages['es']
        return MessageDTO(**messages)
