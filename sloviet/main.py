import asyncio
from sloviet.blaseball import Game
from sloviet.cipher import OneTimePadCipher
from sloviet.encoder import CheckerboardEncoder


def main():
    game = Game('1bf2ec1a-4df8-4446-b7f0-55ba901d4f30')
    encoder = CheckerboardEncoder('blaseboard.cfg')
    cipher = OneTimePadCipher('otp.txt')

    async def handle_event():
        async for event in game.get_events():
            plaincode = encoder.encode(event['description'])
            print(cipher.encrypt(plaincode))

    loop = asyncio.get_event_loop()
    loop.create_task(handle_event())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()