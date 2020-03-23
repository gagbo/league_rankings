from ..lr.league import League
from ..lr.standings import LeagueRulesFFBB
import datetime


def test_92_D1_all_games():
    league = League.from_ffbb_copy_paste("data/ffbb.dat")
    rule_engine = LeagueRulesFFBB(league)
    rule_engine.compute_standings(lambda x: x.played)
    standings = rule_engine.current_standings_sorted_classic
    assert standings[0].name == "CLICHY BASKET ACADEMY"
    assert standings[3].name == "AAE GARENNE COLOMBES"
    assert standings[1].points == 25
    assert standings[2].points == 25
    assert standings[1].name == "COM BAGNEUX - 1"
    assert standings[3].points_scored == 1096
    assert standings[3].points_against == 910

def test_92_D1_date_filter():
    league = League.from_ffbb_copy_paste("data/ffbb.dat")
    rule_engine = LeagueRulesFFBB(league)
    rule_engine.compute_standings(lambda x: x.played and x.date < datetime.datetime(2020, 1, 20))
    standings = rule_engine.current_standings_sorted_classic
    assert standings[0].name == "CLICHY BASKET ACADEMY"
    assert standings[1].name == "AAE GARENNE COLOMBES"
    assert standings[0].points == 19
    assert standings[1].points == 19
    assert standings[3].games_played == 11
    assert standings[3].points_scored == 679
    assert standings[3].points_against == 668
    assert standings[11].games_played == 10


# TODO : add a test that fails currently with the implementation of LeagueRulesFFBB
# It should fail when the matchup point average is different from the global point
# average.
