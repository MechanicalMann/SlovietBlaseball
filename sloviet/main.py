import asyncio
from sloviet.blaseball.messaging import GameAdapter
from sloviet.messaging import ConsoleHandler, MessagePipeline
from sloviet.blaseball.events import Game
from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder


def main():
    game = Game('1bf2ec1a-4df8-4446-b7f0-55ba901d4f30')
    encoder = CheckerboardEncoder('blaseboard.cfg')
    cipher = OneTimePadCipher('otp.txt')
    adapter = GameAdapter(encoder)
    pipeline = MessagePipeline(adapter, [encoder, cipher, ConsoleHandler()])

    game.register(pipeline)

    loop = asyncio.get_event_loop()
    loop.create_task(game.get_events())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()