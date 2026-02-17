import pandas as pd
import utils

def export_normalized_data(df):  
    dfMatch = makeMatchTable(df)
    dfTeam = makeTeamTable(df)
    dfPlayer = makePlayerTable(df)
    dfStatistic = makeStatisticTable(df)
    dfStandings = makeStandingsTable(dfTeam, dfMatch)

    dfOutputs = [dfMatch, dfTeam, dfPlayer, dfStatistic, dfStandings]
    utils.outputTables(dfOutputs)

def makeTeamTable(df):
    return df[['team_id', 'team_name']].drop_duplicates().reset_index(drop=True).sort_values(by=["team_id"])

def makePlayerTable(df):
    return df[['player_id', 'team_id', 'player_name']].drop_duplicates().reset_index(drop=True).sort_values(by=["player_id"])

def makeMatchTable(df):
    dfMatch = None
    home_teams = None
    away_teams = None
    team_goals = None
    home_goals = None
    away_goals = None

    home_teams = (
        df[df["is_home"] == "True"]
        .groupby("match_id")
        .agg(
            match_name=("match_name", "first"),
            home_team_id=("team_id", "first"),
        )
    )

    away_teams = (
        df[df["is_home"] == "False"]
        .groupby("match_id")
        .agg(
            away_team_id=("team_id", "first"),
        )
    )

    team_goals = (
        df.groupby(["match_id", "team_id", "is_home"])["goals_scored"]
        .sum()
        .reset_index()
    )

    home_goals = (
        team_goals[team_goals["is_home"] == "True"]
        .set_index("match_id")["goals_scored"]
    )

    away_goals = (
        team_goals[team_goals["is_home"] == "False"]
        .set_index("match_id")["goals_scored"]
    )

    dfMatch = home_teams.join(away_teams)
    dfMatch["home_goals"] = home_goals
    dfMatch["away_goals"] = away_goals
    dfMatch = dfMatch.reset_index()

    return dfMatch

def makeStatisticTable(df):
    total_match_goals = (
        df.groupby('match_id')['goals_scored']
        .transform('sum')
    )
    dfStatistic = df.copy()
    dfStatistic = dfStatistic[['player_id', 'match_id',
                            'goals_scored', 'minutes_played']]
    dfStatistic.insert(0, 'stat_id', range(1, len(dfStatistic) + 1))
    dfStatistic['fraction_minutes_played'] = dfStatistic['minutes_played'] / 90
    dfStatistic['fraction_goals_scored'] = (
        dfStatistic['goals_scored'] / total_match_goals
    ).fillna(0)

    return dfStatistic.sort_values(by=["player_id","match_id"])

def makeStandingsTable(dfTeam, dfMatch):
    home = None
    away = None
    team_matches = None
    standings = None

    home = dfMatch[["match_id", "home_team_id", "home_goals", "away_goals"]].copy()
    home = home.rename(columns={
        "home_team_id": "team_id",
        "home_goals": "goals_for",
        "away_goals": "goals_against"
    })

    away = dfMatch[["match_id", "away_team_id", "away_goals", "home_goals"]].copy()
    away = away.rename(columns={
        "away_team_id": "team_id",
        "away_goals": "goals_for",
        "home_goals": "goals_against"
    })

    team_matches = pd.concat([home, away], ignore_index=True)

    team_matches["Won"] = (team_matches["goals_for"] > team_matches["goals_against"]).astype(int)
    team_matches["Drawn"] = (team_matches["goals_for"] == team_matches["goals_against"]).astype(int)
    team_matches["Lost"] = (team_matches["goals_for"] < team_matches["goals_against"]).astype(int)

    standings = (
        team_matches
        .groupby("team_id", as_index=False)
        .agg(
            Played=("match_id", "nunique"),
            Won=("Won", "sum"),
            Drawn=("Drawn", "sum"),
            Lost=("Lost", "sum"),
            Goals_For=("goals_for", "sum"),
            Goals_Against=("goals_against", "sum"),
        )
    )

    standings["Goal_Difference"] = standings["Goals_For"] - standings["Goals_Against"]
    standings["Points"] = standings["Won"] * 3 + standings["Drawn"]

    standings = standings.merge(dfTeam[["team_id", "team_name"]], on="team_id", how="left")

    standings = standings.sort_values(
        by=["Points", "Goal_Difference", "Goals_For", "team_name"],
        ascending=[False, False, False, True],
        kind="mergesort"
    ).reset_index(drop=True)

    standings["Rank"] = standings.index + 1

    standings = standings[
        ["Rank", "team_id", "team_name", "Played", "Won", "Drawn", "Lost",
         "Goals_For", "Goals_Against", "Goal_Difference", "Points"]
    ]

    return standings