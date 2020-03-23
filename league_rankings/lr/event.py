import dataclasses
import datetime
from typing import Optional, Tuple


@dataclasses.dataclass(frozen=True)
class Event:
    """
    Represent an event in the league.
    """

    home_team: str = "home"
    away_team: str = "away"
    score: Tuple[int, int] = (0, 0)
    date: datetime.datetime = datetime.datetime.now()
    hasOvertime: bool = False
    played: bool = True

    @property
    def home_points_scored(self) -> int:
        """
        Return the points scored by home team
        """
        return self.score[0]

    @property
    def home_points_against(self) -> int:
        """
        Return the points scored against home team
        """
        return self.score[1]

    @property
    def home_point_differential(self) -> int:
        """
        Return the point differential on the event for home team
        """
        return self.home_points_scored - self.home_points_against

    @property
    def away_points_scored(self) -> int:
        """
        Return the points scored by away team
        """
        return self.score[1]

    @property
    def away_points_against(self) -> int:
        """
        Return the points scored against away team
        """
        return self.score[0]

    @property
    def away_point_differential(self) -> int:
        """
        Return the point differential on the event for away team
        """
        return self.away_points_scored - self.away_points_against

    @property
    def winner(self) -> Optional[str]:
        """
        Return the name of the winning side
        """
        if self.score[0] == self.score[1]:
            return None
        return self.home_team if self.score[0] > self.score[1] else self.away_team

    @property
    def winner_points_scored(self) -> int:
        """
        Return the points scored by winning side. Return the identical score in case
        of draw.
        """
        return max(self.score)

    @property
    def winner_points_against(self) -> int:
        """
        Return the points scored against winning side. Return the identical score in case
        of draw.
        """
        return min(self.score)

    @property
    def winner_point_differential(self) -> int:
        """
        Return the point differential for winning side. Return 0 in case of draw.
        """
        return self.winner_points_scored - self.winner_points_against

    @property
    def loser(self) -> Optional[str]:
        """
        Return the name of the losing side
        """
        if self.score[0] == self.score[1]:
            return None
        return self.away_team if self.score[0] > self.score[1] else self.home_team

    @property
    def loser_points_scored(self) -> int:
        """
        Return the points scored by losing side. Return the identical score in case
        of draw.
        """
        return min(self.score)

    @property
    def loser_points_against(self) -> int:
        """
        Return the points scored against losing side. Return the identical score in case
        of draw.
        """
        return max(self.score)

    @property
    def loser_point_differential(self) -> int:
        """
        Return the point differential for losing side. Return 0 in case of draw.
        """
        return self.loser_points_scored - self.loser_points_against
