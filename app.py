import pandas as pd
import normalize as nl
import clean as cl


#input denormalised data
df = pd.read_csv('assignment_input.csv', encoding='ISO-8859-1')

df = cl.export_anomalies_and_clean_data(df)
nl.export_normalized_data(df)
