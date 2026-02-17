import pandas as pd
from normalize import makeMatchTable
from normalize import makeStandingsTable

def test_build_match_returns_dataframe():
    test_df = pd.DataFrame({
        "match_id": [1,1],
        "match_name": ["A vs B","A vs B"],
        "team_id": [10,20],
        "team_name": ["A","B"],
        "is_home": [True, False],
        "player_id": [1,2],
        "player_name": ["P1","P2"],
        "goals_scored": [1,0],
        "minutes_played": [90,90]
    })

    result = makeMatchTable(test_df)

    assert isinstance(result, pd.DataFrame)

def test_match_goal_calculation():
    df = pd.DataFrame({
        "match_id": [1,1],
        "match_name": ["A vs B","A vs B"],
        "team_id": [10,20],
        "is_home": ["True","False"],
        "goals_scored": [2,1]
    })

    result = makeMatchTable(df)

    assert result.iloc[0]["home_goals"] == 2
    assert result.iloc[0]["away_goals"] == 1

def test_points_and_ranking():
    dfMatch = pd.DataFrame({
        "match_id": [1],
        "home_team_id": [10],
        "away_team_id": [20],
        "home_goals": [2],
        "away_goals": [1]
    })

    df = pd.DataFrame({
        "team_id": [10,20],
        "team_name": ["A","B"]
    })

    standings = makeStandingsTable(df, dfMatch)

    assert standings.iloc[0]["team_id"] == 10
    assert standings.iloc[0]["Points"] == 3