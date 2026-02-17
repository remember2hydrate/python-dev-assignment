import pandas as pd
from clean import cleanNegatives
from clean import cleanCrossTeamed
from clean import cleanIdNameMismatch

def test_clean_negatives_detects_invalid_rows():
    df = pd.DataFrame({
        "match_id": [1, -1],
        "team_id": [10, 20],
        "player_id": [100, 101],
        "goals_scored": [1, -2],
        "minutes_played": [90, 80]
    })

    result = cleanNegatives(df)

    assert len(result) == 1
    assert result.iloc[0]["match_id"] == -1

def test_cross_team_violation():
    df = pd.DataFrame({
        "player_id": [1, 1, 2],
        "team_id": [10, 11, 20]
    })

    result = cleanCrossTeamed(df)

    assert result["player_id"].nunique() == 1
    assert result["player_id"].iloc[0] == 1

def test_id_name_mismatch_detected():
    df = pd.DataFrame({
        "match_id": [1, 1],
        "match_name": ["A vs B", "Different Name"],
        "team_id": [10, 10],
        "team_name": ["A", "A"],
        "player_id": [1, 1],
        "player_name": ["P1", "P1"]
    })

    result = cleanIdNameMismatch(df)

    assert len(result) == 2