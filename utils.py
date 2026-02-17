anomalies_path = "output/anomalies.jsonl"
match_path = "output/match.jsonl"
team_path = "output/team.jsonl"
player_path = "output/player.jsonl"
statistic_path = "output/statistic.jsonl"
standings_path = "output/standings.jsonl"
output_paths = [match_path,team_path,player_path,statistic_path, standings_path]

def output(pathOut,dfOut) : 
    with open(pathOut, "w", encoding='utf-8') as f:
        f.write(dfOut.to_json(orient='records', lines=True, force_ascii=False))

def outputTables(dfOutputs):
    for path, df in zip(output_paths, dfOutputs):
        output(path, df)

def outputAnomalies(df):
    output(anomalies_path,df)