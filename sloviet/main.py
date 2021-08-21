import argparse, asyncio, os, sys
from sloviet.reader import Reader
from sloviet.blaseball.messaging import GameAdapter
from sloviet.messaging import ConsoleHandler, GroupFormatHandler, MessagePipeline
from sloviet.blaseball.events import Game
from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder

parser = argparse.ArgumentParser(
    prog='sloviet.py',
    description=
    'Generate a numbers station broadcast describing a Blaseball game play-by-play.'
)
parser.add_argument(
    '-s',
    '--skip-headers',
    default=False,
    const=True,
    action='store_const',
    help='When set, skips sending WAV RIFF header bytes for each digit.')
parser.add_argument(
    '-t',
    '--text-only',
    default=False,
    const=True,
    action='store_const',
    help=
    'When set, the output will be the text of all encrypted messages instead of audio.'
)
parser.add_argument('game_id')


def main():
    args = parser.parse_args()

    if args.text_only:
        reader = ConsoleHandler()
    else:
        reader = Reader(args.skip_headers)
        reader.load('audio', 0.75)

    game = Game(args.game_id)
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
    if hasattr(reader, 'read'):
        loop.create_task(reader.read())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()