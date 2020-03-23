from ..lib.event import Event


def test_winner():
    home_win = Event(home_team="HOME", away_team="AWAY", score=(65, 64))
    assert home_win.winner == "HOME"
    assert home_win.winner_points_against == 64
    assert home_win.winner_points_scored == 65
    assert home_win.winner_point_differential == 1

    away_win = Event(home_team="HOME", away_team="AWAY", score=(82, 101))
    assert away_win.winner == "AWAY"
    assert away_win.winner_points_against == 82
    assert away_win.winner_points_scored == 101
    assert away_win.winner_point_differential == 19

    draw = Event(home_team="HOME", away_team="AWAY", score=(58, 58))
    assert draw.winner is None
    assert draw.winner_points_against == 58
    assert draw.winner_points_scored == 58
    assert draw.winner_point_differential == 0


def test_loser():
    home_win = Event(home_team="HOME", away_team="AWAY", score=(65, 64))
    assert home_win.loser == "AWAY"
    assert home_win.loser_points_against == 65
    assert home_win.loser_points_scored == 64
    assert home_win.loser_point_differential == -1

    away_win = Event(home_team="HOME", away_team="AWAY", score=(82, 101))
    assert away_win.loser == "HOME"
    assert away_win.loser_points_against == 101
    assert away_win.loser_points_scored == 82
    assert away_win.loser_point_differential == -19

    draw = Event(home_team="HOME", away_team="AWAY", score=(58, 58))
    assert draw.loser is None
    assert draw.loser_points_against == 58
    assert draw.loser_points_scored == 58
    assert draw.loser_point_differential == 0


def test_points_scored():
    home_win = Event(home_team="HOME", away_team="AWAY", score=(65, 44))
    assert home_win.home_points_scored == 65
    assert home_win.away_points_scored == 44


def test_points_against():
    away_win = Event(home_team="HOME", away_team="AWAY", score=(72, 94))
    assert away_win.home_points_against == 94
    assert away_win.away_points_against == 72


def test_point_differential():
    home_win = Event(home_team="HOME", away_team="AWAY", score=(92, 84))
    assert home_win.home_point_differential == 8
    assert home_win.away_point_differential == -8
