import asyncio
from blaseball_mike import database as datablase, eventually


class Game(object):
    def __init__(self, game_id: str) -> None:
        self.id = game_id
        game = datablase.get_game_by_id(game_id)
        if not game:
            raise ValueError('Invalid game ID')

    async def get_events(self):
        for event in eventually.search(limit=-1,
                                       query={
                                           'gameTags': [self.id],
                                           'sortorder': 'asc'
                                       }):
            yield event
            await asyncio.sleep(5)  # roughly approximate a real game feed
