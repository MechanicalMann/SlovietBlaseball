import asyncio
import os, re, sys
import multiprocessing as mp
from asyncio import Queue
from typing import Dict
from sloviet.messaging import Message, MessageHandler


class Reader(mp.Process, MessageHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._queue: Queue[Message] = Queue()
        self._numbers: Dict[str, bytes] = {}
        self._chars = ' 0123456789'
        self.duration = 0.0

    def load(self, dir: str, duration: float) -> None:
        self.duration = duration
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            digit = re.match(r'(\d).wav', filename)
            if not digit:
                continue
            with open(os.path.join(dir, filename), 'rb') as f:
                self._numbers[digit[1]] = f.read()
        if not len(self._numbers) == 10:
            raise ValueError('Invalid audio directory')

    def add_message(self, message: Message):
        self._queue.put_nowait(message)

    def handle(self, message: Message):
        self.add_message(message)

    async def read(self):
        while True:
            message = await self._queue.get()
            for c in message.content:
                if not c in self._chars:
                    continue
                digit = self._numbers.get(c)
                if digit:
                    sys.stdout.buffer.write(digit)
                    # sys.stdout.buffer.flush()
                await asyncio.sleep(self.duration)
