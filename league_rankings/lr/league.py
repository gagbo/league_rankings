from .event import Event
from typing import List, Iterable, Set
import re
import datetime
import csv


class League:
    """
    Collection of events with smart rankings.
    """

    events: List[Event]
    valid_teams: Set[str]

    def __init__(
        self, *, teams: Iterable[str] = None, some_events: Iterable[Event] = None
    ):
        self.valid_teams = set()
        self.events = list()
        if teams:
            for team in teams:
                self.add_valid_team(team)
        if some_events:
            for event in some_events:
                self.add_event(event)

    def add_valid_team(self, team_name: str) -> None:
        self.valid_teams.add(team_name)

    def add_events(self, events: Iterable[Event]) -> None:
        for event in events:
            self.add_event(event)

    def add_event(self, event: Event) -> None:
        if event.home_team not in self.valid_teams:
            raise ValueError(f"{event.home_team} is not a team in this league !")
        if event.away_team not in self.valid_teams:
            raise ValueError(f"{event.away_team} is not a team in this league !")
        self.events.append(event)
        self.events.sort(key=lambda x: x.date)

    def __iter__(self):
        return LeagueGamesIterator(self)

    @classmethod
    def from_ffbb_copy_paste(cls, filepath: str) -> "League":
        teams = set()
        some_events: List[Event] = list()
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter="	")
            DATE = 1
            HOUR = 2
            HOME_TEAM = 3
            AWAY_TEAM = 4
            SCORE = 5
            score_regex = re.compile(r"(?P<home_score>\d+) - (?P<away_score>\d+)")
            for row in reader:
                teams.add(row[HOME_TEAM])
                teams.add(row[AWAY_TEAM])
                score = (-1, -1)
                match = score_regex.match(row[SCORE])
                if match is not None:
                    score = (
                        int(match.group("home_score")),
                        int(match.group("away_score")),
                    )
                played = score != (-1, -1)
                str_timestamp = row[DATE] + " " + row[HOUR]
                timestamp = datetime.datetime.strptime(str_timestamp, "%d/%m/%Y %H:%M")
                some_events.append(
                    Event(
                        home_team=row[HOME_TEAM],
                        away_team=row[AWAY_TEAM],
                        date=timestamp,
                        score=score,
                        played=played,
                    )
                )
        return cls(teams=teams, some_events=some_events)


def LeagueGamesIterator(league: League):
    """
    Iterator to iterate over all games of a league
    """
    for event in league.events:
        yield event


