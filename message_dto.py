from dataclasses import dataclass

@dataclass
class MessageDTO:
    no_elements_active: str
    consider_active_elements: str
    enter_search_term: str
    names_not_found: str
    elements_found: str