import pandas as pd

# convert the csv into a dataframe
df = pd.read_csv("desktop_app/test_qna.csv", sep=";")

# utillities
print(df.head())