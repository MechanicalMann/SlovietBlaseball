from abc import ABC, abstractmethod
import string


class Encoder(ABC):
    @abstractmethod
    def encode(self, plaintext: str) -> str:
        pass


class RingEncoder(Encoder):
    def __init__(self, charmap: str = None) -> None:
        if not charmap:
            # Hail, Caesar!
            charmap = string.ascii_lowercase[-3:] + string.ascii_lowercase[:-3]
        self.map = dict(zip(string.ascii_lowercase, charmap.lower()))

    def get_char(self, char: str):
        if len(char) == 1 and (c := char.lower()) in self.map:
            return self.map[c].upper() if char.isupper() else self.map[c]
        return char

    def encode(self, plaintext: str):
        return ''.join([self.get_char(c) for c in plaintext])