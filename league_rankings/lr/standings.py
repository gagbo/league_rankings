from .league import League
from .event import Event
from typing import Dict, Callable, List
import dataclasses

@dataclasses.dataclass
class StandingEntry:
    """
    A "row" of standings
    """

    name: str
    points: int = 0
    points_scored: int = 0
    points_against: int = 0
    games_played: int = 0

    def __str__(self) -> str:
        return "\t".join(
            [
                self.name,
                str(self.points) + " Pts",
                "(" + str(self.games_played) + ")",
                "(" + str(self.points_scored) + " - " + str(self.points_against) + ")",
            ]
        )



class RuleEngine:
    """
    Rule engine regarding points per encounter etc.
    """

    results: League
    standings: Dict[str, StandingEntry]

    def __init__(self, league: League):
        self.results = league
        self.standings = dict()
        for team in self.results.valid_teams:
            self.standings.setdefault(team, StandingEntry(name=team))
        self.points_per_win = 2
        self.points_per_loss = 1

    def compute_standings(self, filter: Callable[[Event], bool]):
        for event in self.results:
            if filter(event) is False:
                continue
            self.standings = self.compute_event(event, self.standings)

    @property
    def current_standings_sorted_classic(self) -> List[StandingEntry]:
        return sorted(
            [entry for entry in self.standings.values()],
            key=lambda entry: entry.points
            + 0.001 * (entry.points_scored - entry.points_against)
            + 0.0000001 * entry.points_scored,
            reverse=True,
        )

    @property
    def current_standings_raw(self) -> Dict[str, StandingEntry]:
        """
        Return the standings raw for any ordering you want
        """
        return self.standings

    def compute_event(
        self, event: Event, old_state: Dict[str, StandingEntry]
    ) -> Dict[str, StandingEntry]:
        raise NotImplemented



class LeagueRulesFFBB(RuleEngine):
    """
    Rule specific to classic FFBB Rules
    - No draw
    - 2 points per win
    - 1 point per loss
    """

    def __init__(self, league: League):
        super().__init__(league)
        self.points_per_win = 2
        self.points_per_loss = 1
        # TODO : Also store the per-matchup point average, since in
        # this rule set, this is the primary tie-breaker

    def compute_event(
        self, event: Event, old_state: Dict[str, StandingEntry]
    ) -> Dict[str, StandingEntry]:
        new_state = old_state
        if event.played:
            new_state[event.home_team].games_played += 1
            new_state[event.away_team].games_played += 1
        if event.winner is not None and event.loser is not None:
            new_state[event.winner].points += self.points_per_win
            new_state[event.winner].points_scored += event.winner_points_scored
            new_state[event.winner].points_against += event.winner_points_against
            new_state[event.loser].points += self.points_per_loss
            new_state[event.loser].points_scored += event.loser_points_scored
            new_state[event.loser].points_against += event.loser_points_against
        else:
            raise ValueError("No draw by FFBB Rules ! So each event has a winner and a loser")

        return new_state
