from abc import ABC, abstractmethod
from typing import List


class Event(ABC):
    pass


class EventListener(ABC):
    @abstractmethod
    def listen(self, event: Event):
        pass


class EventEmitter(ABC):
    listeners: List[EventListener] = []

    @abstractmethod
    async def get_events(self):
        pass

    def emit(self, event: Event):
        for listener in self.listeners:
            listener.listen(event)

    def register(self, listener: EventListener):
        self.listeners.append(listener)
