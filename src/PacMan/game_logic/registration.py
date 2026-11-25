
from dataclasses import dataclass
from src.PacMan.app_config.config import REGISTRATION_TRIES


@dataclass(frozen=True)
class RegistrationSnapshot:
    payload: str
    message: str


class TriesError(Exception):
    pass


class RegisterError(Exception):
    pass


class RegistrationProcess:
    def __init__(self) -> None:
        self.tries: int = REGISTRATION_TRIES
        self.payload: str = ""
        self.default_message: str = ("Please enter name. "
                                     "Allowed characters: A-Z, a-z,"
                                     " 0-9, space, backspace. ")
        self.custom_message: str = ""

    def view(self) -> RegistrationSnapshot:
        message_ss = (self.default_message +
                      self.custom_message +
                      self._tries_message())
        return RegistrationSnapshot(payload=self.payload,
                                    message=message_ss)

    def add_char_to_payload(self, char: str) -> None:
        self.custom_message = ""
        try:
            new_char = self._char_validity(char)
        except RegisterError as e:
            self.custom_message = str(e) + " "
        if new_char == '\b':
            self.payload = self.payload[:-1]
        else:
            self.payload += new_char

    @staticmethod
    def _char_validity(char: str) -> str:
        if not isinstance(char, str):
            raise RegisterError("Char must be a string.")
        if len(char) != 1:
            raise RegisterError("Exactly one character is required.")
        if not (char.isascii() and (char.isalnum()
                                    or char == ' '
                                    or char == '\b')):
            raise RegisterError("Only ASCII letters, numbers, space"
                                " and backspace are allowed.")
        return char

    def get_name(self) -> str | None:
        self.custom_message = ""
        self._decrement_tries()
        try:
            return self._validate_payload(self.payload)
        except RegisterError as e:
            self.custom_message = str(e) + " "
        return None

    def _decrement_tries(self) -> None:
        self.tries -= 1
        if self.tries <= 0:
            raise TriesError("No more tries left.")

    @staticmethod
    def _validate_payload(payload: str) -> str:
        if not isinstance(payload, str):
            raise RegisterError("Name must be a string.")
        if len(payload) <= 1 or len(payload) >= 20:
            raise RegisterError("Name can be between one "
                                "and twenty characters.")
        for char in payload:
            if not (char.isascii() and (char.isalnum()
                                        or char == ' ')):
                raise RegisterError("Only ASCII letters, numbers and space"
                                    " are allowed.")
        return payload

    def _tries_message(self) -> str:
        return (f"{self.tries} tries left before "
                "registration exits. ")
