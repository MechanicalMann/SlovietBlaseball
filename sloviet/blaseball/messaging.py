from sloviet.blaseball.types import EventType
from sloviet.encoder import CheckerboardEncoder
from sloviet.messaging import Message, MessageAdapter
from sloviet.blaseball.events import GameEvent


class GameAdapter(MessageAdapter):
    def __init__(self, checkerboard: CheckerboardEncoder) -> None:
        self.characters = checkerboard.config['CodeCharacters']
        self.figure_code = self.characters.get('FIGURE', '')

    def char(self, type: str, default=''):
        if not type in self.characters:
            return default
        c = self.characters[type]
        return c

    def code(self, number: int):
        return f'!{number:03d}'

    def count(self, event: GameEvent):
        balls = self.char('COUNT_BALLS', 'B')
        strikes = self.char('COUNT_STRIKES', 'S')
        return f'{balls}{event.balls}{self.figure_code}{strikes}{event.strikes}{self.figure_code}'

    def outs(self, event: GameEvent, force=False):
        if not force and event.outs == event.game.prev.outs:
            return ''
        if event.outs == 0: # The last out in the inning clears all the counts
            return ''
        outs = self.char('COUNT_OUTS', 'O')
        return f'{outs}{event.outs}{self.figure_code}'

    def score(self, event: GameEvent, force=False):
        if not force and event.inning_runs == event.game.prev.inning_runs:
            return ''
        home = self.char('TEAM_HOME', 'H')
        away = self.char('TEAM_AWAY', 'A')
        return f'{away}{event.away_score}{self.figure_code}{home}{event.home_score}{self.figure_code}'

    def adapt(self, event: GameEvent) -> Message:
        if event.type == EventType.LETS_GO:
            start = self.char('LETS_GO') or self.code(EventType.LETS_GO)
            home = self.char('TEAM_HOME')
            away = self.char('TEAM_AWAY')
            weather = self.char('WEATHER') or self.code(EventType.WEATHER_CHANGE)
            return Message(f'{start}{away}{event.game.away_team_nick}{home}{event.game.home_team_nick}{weather}{event.game.weather_id}{self.figure_code}')
        if event.type == EventType.PLAY_BALL:
            home = self.char('TEAM_HOME')
            away = self.char('TEAM_AWAY')
            pitcher = self.char('PITCHER')
            return Message(f'{away}{pitcher}{event.game.away_pitcher}{home}{pitcher}{event.game.home_pitcher}')
        if event.type == EventType.INNING_CHANGE:
            inning = self.char('INNING') or self.code(event.type)
            number = event.inning
            half = 'top' if event.top else 'bot'
            return Message(f'{inning}{half}{number}')
        if event.type == EventType.STRIKEOUT:
            strikeout = self.char('STRIKEOUT') or self.code(event.type)
            batter = event.game.prev.batter
            return Message(f'{strikeout}{batter}{self.outs(event)}')
        if event.type == EventType.FLYOUT:
            flyout = self.char('FLYOUT') or self.code(event.type)
            batter = event.game.prev.batter
            return Message(f'{flyout}{batter}{self.outs(event)}')
        if event.type == EventType.GROUNDOUT:
            groundout = self.char('GROUNDOUT') or self.code(event.type)
            batter = event.game.prev.batter
            return Message(f'{groundout}{batter}{self.outs(event)}')
        if event.type == EventType.HOME_RUN:
            home_run = self.char('HOME_RUN') or self.code(event.type)
            batter = event.game.prev.batter
            return Message(f'{home_run}{self.score(event)}')
        if event.type == EventType.HIT:
            hit = self.char('HIT') or self.code(event.type)
            batter = event.game.prev.batter
            return Message(f'{hit}{batter}{self.score(event)}{self.outs(event)}')
        if event.type == EventType.WALK:
            walk = self.char('WALK')
            runner = event.game.prev.batter
            return Message(f'{walk}{runner}{self.score(event)}')
        if event.type == EventType.PITCHER_CHANGE:
            change = self.char('PITCHER') or self.code(event.type)
            if event.top:
                team = self.char('TEAM_AWAY') or event.game.away_team
                pitcher = event.away_pitcher
            else:
                team = self.char('TEAM_HOME') or event.game.home_team
                pitcher = event.home_pitcher
            return Message(f'{change}{team}{pitcher}')
        if event.type == EventType.NOW_BATTING:
            change = self.char('AT_BAT') or self.code(event.type)
            if event.top:
                team = self.char('TEAM_AWAY') or event.game.away_team
            else:
                team = self.char('TEAM_HOME') or event.game.home_team
            batter = event.batter
            return Message(f'{change}{team}{batter}')
        if event.type == EventType.BALL:
            ball = self.char('BALL') or self.code(event.type)
            return Message(f'{ball}{self.count(event)}')
        if event.type == EventType.STRIKE:
            strike = self.char('STRIKE') or self.code(event.type)
            return Message(f'{strike}{self.count(event)}')
        if event.type == EventType.FOUL:
            foul = self.char('FOUL') or self.code(event.type)
            return Message(f'{foul}{self.count(event)}')
        if event.type == EventType.END_OF_INNING:
            end = self.char('END_OF_INNING') or self.code(event.type)
            return Message(f'{end}{self.score(event, force=True)}')

        # Fallback for events with codes that we don't have special handling for
        if event.type:
            return Message(f'{self.code(event.type)}{self.count(event)}{self.outs(event)}{self.score(event)}')

        if not event.type and not event.description and not event.game_started:
            return # Blank event

        # Last-ditch fallback
        return Message(event.description)
