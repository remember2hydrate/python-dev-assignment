import utils 

def export_anomalies_and_clean_data(df):
    #clean data
    dfNegative = cleanNegatives(df)
    dfMinutesOver = cleanOver90(df)
    dfisHomeNotBoolean = cleanNotBoolean(df)
    dfCrossTeam = cleanCrossTeamed(df)
    dfIdNameMismatch = cleanIdNameMismatch(df)
    dfTeamNameNotIncludedInMatch = cleanExcludedTeamNames(df)
    dfWithQuotes = cleanQuoted(df)
    dfMissingInfo = cleanMissingInfo(df)
    
    #append to anomalies jsonl 
    dfAnomalies = dfNegative._append(dfMinutesOver, ignore_index=False) 
    dfAnomalies = dfAnomalies._append(dfisHomeNotBoolean, ignore_index=False) 
    dfAnomalies = dfAnomalies._append(dfCrossTeam, ignore_index=False)
    dfAnomalies = dfAnomalies._append(dfIdNameMismatch, ignore_index=False)
    dfAnomalies = dfAnomalies._append(dfTeamNameNotIncludedInMatch, ignore_index=False)
    dfAnomalies = dfAnomalies._append(dfWithQuotes, ignore_index=False)
    dfAnomalies = dfAnomalies._append(dfMissingInfo, ignore_index=False)

    utils.outputAnomalies(dfAnomalies)
    #drop anomaly rows from dataframe
    df.drop(dfAnomalies.index, inplace=True)
    return df

def cleanNegatives(df):
    # violation negative numbers - NEGATIVE goals, minutes 
    dfNegative = df.query("match_id < 0 | team_id < 0 | player_id < 0  | goals_scored  < 0  | minutes_played  < 0")
    dfNegative.insert(0,"violation description","negative id, minute or goal")
    return dfNegative
    
def cleanOver90(df):
    # violation invalid minutes - MINUTES over 90!
    dfMinutesOver = df.query("minutes_played > 90")
    dfMinutesOver.insert(0,"violation description", "invalid minutes - MINUTES over 90!")
    return dfMinutesOver

def cleanNotBoolean(df):
    # violation isHomeNotBoolean
    dfisHomeNotBoolean = df[~df['is_home'].isin([True, False, "True", "False"])].copy() 
    dfisHomeNotBoolean.insert(0,"violation description", "invalid boolean") 
    return dfisHomeNotBoolean

def cleanCrossTeamed(df):
    #violation Cross-team violation 
    dfCrossTeam = df[df.groupby('player_id')['team_id'].transform('nunique') > 1].copy()
    dfCrossTeam.insert(0,"violation description", "Cross-team violation")
    return dfCrossTeam

def cleanIdNameMismatch(df):
    #violation id-Name mismatch for teams,players,matches
    dfIdNameMismatch = df[ 
        (df.groupby('match_id')['match_name'].transform('nunique') > 1) |
        (df.groupby('team_id')['team_name'].transform('nunique') > 1) |
        (df.groupby('player_id')['player_name'].transform('nunique') > 1)
    ].copy()
    dfIdNameMismatch.insert(0,"violation description", "id - name mismatch for team, player or match")
    return dfIdNameMismatch

def cleanExcludedTeamNames(df):
    #violation team name not included in match name
    teams_in_match = df['match_name'].str.split(' vs ', expand=True)
    dfTeamNameNotIncludedInMatch = df[
        (df['team_name'] != teams_in_match[0]) &
        (df['team_name'] != teams_in_match[1])
    ].copy()
    dfTeamNameNotIncludedInMatch.insert(0,"violation description", "team name not included in match name violation")
    return dfTeamNameNotIncludedInMatch

def cleanQuoted(df):
    #violation unexpected quotes
    dfWithQuotes = df[
        df.select_dtypes(include='object').apply(lambda col: col.str.contains('"""', na=False))
                .any(axis=1)
    ].copy()
    dfWithQuotes.insert(0, "violation description", "unexpected quote in string value")
    return dfWithQuotes

def cleanMissingInfo(df):
    #violation missing fields
    required_fields = ["match_id","match_name","team_id","team_name", "is_home","player_id","player_name","goals_scored","minutes_played"]
    mask_missing = df[required_fields].isnull().any(axis=1)
    dfMissing = df[mask_missing].copy()
    dfMissing.insert(0, "violation description", "missing required field(s)")
    return dfMissing