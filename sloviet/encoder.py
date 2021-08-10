from abc import ABC, abstractmethod
import configparser
import string


class Encoder(ABC):
    def encode(self, plaintext: str) -> str:
        return ''.join([self.get_char(c) for c in plaintext])

    @abstractmethod
    def get_char(self, char: str) -> str:
        pass


class RingEncoder(Encoder):
    def __init__(self, charmap: str = None) -> None:
        if not charmap:
            # Hail, Caesar!
            charmap = string.ascii_lowercase[-3:] + string.ascii_lowercase[:-3]
        self.map = dict(zip(string.ascii_lowercase, charmap.lower()))

    def get_char(self, char: str) -> str:
        if len(char) == 1 and (c := char.lower()) in self.map:
            return self.map[c].upper() if char.isupper() else self.map[c]
        return char


class CheckerboardEncoder(Encoder):
    def __init__(self, file: str, unknown=False, spaces=False) -> None:
        self.config = configparser.ConfigParser()
        self.unknown = unknown
        self.spaces = spaces
        self.code_chars = {}
        if not file in self.config.read(file):
            raise ValueError('Could not read config file!')
        if not 'Characters' in self.config:
            raise configparser.NoSectionError('Characters')
        if 'CodeCharacters' in self.config:
            self.code_chars = {
                v: k
                for k, v in self.config['CodeCharacters'].items()
            }

    def get_char(self, char: str) -> str:
        if char == ' ' and self.spaces:
            return self.config['Codes'].get('SPACE', '')
        if char in self.code_chars:
            code = self.code_chars[char]
            return self.config['Codes'][code]
        if char in self.config['Characters']:
            return self.config['Characters'][char]
        if self.unknown:
            return char
        return ''
