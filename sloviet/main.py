import asyncio
from sloviet.reader import Reader
from sloviet.blaseball.messaging import GameAdapter
from sloviet.messaging import ConsoleHandler, GroupFormatHandler, MessagePipeline
from sloviet.blaseball.events import Game
from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder


def main():
    reader = Reader()
    reader.load('audio', 0.75)

    game = Game('1bf2ec1a-4df8-4446-b7f0-55ba901d4f30')
    encoder = CheckerboardEncoder('blaseboard.cfg')
    cipher = OneTimePadCipher('otp.txt')
    adapter = GameAdapter(encoder)
    pipeline = MessagePipeline(adapter, [
        encoder,
        cipher,
        GroupFormatHandler(suffix=' 0 0 0  '),
        reader,
    ])

    game.register(pipeline)

    loop = asyncio.get_event_loop()
    loop.create_task(game.get_events())
    loop.create_task(reader.read())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()