import asyncio, os, sys
from sloviet.reader import Reader
from sloviet.blaseball.messaging import GameAdapter
from sloviet.messaging import ConsoleHandler, GroupFormatHandler, MessagePipeline
from sloviet.blaseball.events import Game
from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder


def main():
    if len(sys.argv) < 2:
        exit(1)

    game_id = sys.argv[1]
    reader = Reader()
    reader.load('audio', 0.75)

    game = Game(game_id)
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

    reader.identify(os.getpid(), f'{game.season:03d}', f'{game.day:02d}')

    loop = asyncio.get_event_loop()
    loop.create_task(game.get_events())
    loop.create_task(reader.read())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()