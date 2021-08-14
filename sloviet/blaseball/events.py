import asyncio, json
from sloviet.events import Event, EventEmitter
from blaseball_mike import database as datablase, eventually, chronicler
from sloviet.blaseball.types import guess_event_type

# Surely there's a way we could... not do this
class GameEvent(Event):
    def __init__(self, event: dict, **kwargs) -> None:
        self.id = event['id']
        self.type = None
        self.balls = event['atBatBalls']
        self.strikes = event['atBatStrikes']
        self.outs = event['halfInningOuts']
        self.inning = event['inning'] + 1
        self.top = event['topOfInning']
        self.game_over = event['gameComplete']
        self.away_score = event['awayScore']
        self.home_score = event['homeScore']
        if event['awayBatterName']:
            self.batter = event['awayBatterName']
        else:
            self.batter = event['homeBatterName']
        self.description = None
        if 'lastUpdate' in event and event['lastUpdate']:
            self.description = event['lastUpdate']
            self.type = guess_event_type(self.description)
        for k in kwargs:
            self.__setattr__(k, kwargs[k])



class Game(EventEmitter):
    def __init__(self, game_id: str) -> None:
        self.id = game_id
        game = datablase.get_game_by_id(game_id)
        if not game:
            raise ValueError('Invalid game ID')
        self.home_team = game['homeTeamName']
        self.away_team = game['awayTeamName']
        self.home_pitcher = game['homePitcherName']
        self.away_pitcher = game['awayPitcherName']
        if 'weather' in game and game['weather']:
            self.weather_id = int(game['weather'])
            weather = datablase.get_weather()
            self.weather = weather[self.weather_id]['name']
        if 'stadium' in game and game['stadium']:
            self.stadium_id = game['stadium']
            # There ... might be no way to get the stadium name from the API

    async def get_events(self):
        for event in chronicler.get_game_updates(
                game_ids=['1bf2ec1a-4df8-4446-b7f0-55ba901d4f30'], lazy=True):
            if not 'data' in event:
                continue
            self.emit(GameEvent(event['data'], game=self))
            await asyncio.sleep(5)  # roughly approximate a real game feed
