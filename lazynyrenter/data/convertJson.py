import pandas as pd

myfile = open('aggregatedData.json', 'r').read()

df = pd.read_json(myfile)
df.set_index('id', inplace=True)
df.to_csv('aggregatedData.csv')
