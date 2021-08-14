import secrets
from sloviet.messaging import Message, MessageHandler


class OneTimePadCipher(MessageHandler):
    def __init__(self, padfile: str) -> None:
        with open(padfile) as pf:
            self.pads = {
                s[:5]: s[5:].replace(' ', '').strip()
                for s in pf.readlines()
            }
        self.used = {}

    def encrypt(self, plaintext: str) -> str:
        if len(self.pads) == 0:
            # This is quite insecure
            self.pads.update(self.used)
            self.used.clear()
        id = secrets.choice(list(self.pads.keys()))
        pad = self.pads.pop(id)
        self.used[id] = pad
        while len(plaintext) > len(pad):
            # So is this
            pad = pad + pad
        while not len(plaintext) % 5 == 0:
            plaintext = plaintext + '0'
        numbers = [(int(left), int(right))
                   for left, right in zip(plaintext, pad)]
        result = [str((left - right) % 10) for left, right in numbers]
        return id + ''.join(result)

    def handle(self, message: Message) -> Message:
        return Message(self.encrypt(message.content))