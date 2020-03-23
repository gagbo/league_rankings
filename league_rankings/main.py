from .lr.event import Event
from .lr.league import League
from .lr.standings import LeagueRulesFFBB
from typing import List
import datetime

if __name__ == "__main__":
    print("Hello World")

    league = League.from_ffbb_copy_paste("data/ffbb.dat")

    for game in league:
        print(game)

    print("Classic rules")
    rule_engine = LeagueRulesFFBB(league)
    rule_engine.compute_standings(lambda x: x.played)
    for entry in rule_engine.current_standings_sorted_classic:
        print(str(entry))

    print("Only Phase 1 games")
    rule_engine_2 = LeagueRulesFFBB(league)
    rule_engine_2.compute_standings(
        lambda x: x.played and x.date < datetime.datetime(2020, 1, 20)
    )
    for entry in rule_engine_2.current_standings_sorted_classic:
        print(str(entry))
