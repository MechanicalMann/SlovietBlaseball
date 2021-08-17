from abc import ABC, abstractmethod
from typing import List
from sloviet.events import Event, EventListener


class Message(object):
    def __init__(self, content: str) -> None:
        self.content = content


class MessageAdapter(ABC):
    @abstractmethod
    def adapt(self, event: Event) -> Message:
        pass


class MessageHandler(ABC):
    @abstractmethod
    def handle(self, message: Message) -> Message:
        return message


class MessagePipeline(EventListener):
    def __init__(self,
                 adapter: MessageAdapter,
                 handlers: List[MessageHandler] = []) -> None:
        self.adapter = adapter
        self.handlers = handlers

    def listen(self, event: Event):
        message = self.adapter.adapt(event)
        if not message:
            return
        for handler in self.handlers:
            message = handler.handle(message)
            if not message:
                break

    def register(self, handler: MessageHandler):
        self.handlers.append(handler)


class GroupFormatHandler(MessageHandler):
    def __init__(self, prefix: str = '', suffix: str = '') -> None:
        self.prefix = prefix
        self.suffix = suffix

    def handle(self, message: Message) -> Message:
        grouped = ' '.join([
            message.content[i:i + 5] for i in range(0, len(message.content), 5)
        ])
        return Message(f'{self.prefix}{grouped}{self.suffix}')


class ConsoleHandler(MessageHandler):
    def handle(self, message: Message) -> Message:
        print(message.content)
        return message
