
from sloviet.events import Event
from sloviet.messaging import Message, MessageAdapter
from sloviet.blaseball.events import GameEvent


class GameAdapter(MessageAdapter):
    def adapt(self, event: GameEvent) -> Message:
        if not event.description:
            return
        content = event.description
        # Complexity to come...
        return Message(content)