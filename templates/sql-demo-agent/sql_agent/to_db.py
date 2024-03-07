import pandas as pd

csv = pd.read_csv('data.csv')
csv.to_sql("sqlite:///data.db", if_exists="replace")


