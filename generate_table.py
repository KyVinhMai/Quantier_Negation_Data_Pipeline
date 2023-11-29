import sqlite3
import pandas as pd
connection = sqlite3.connect('E:\AmbiLab_data\quant_neg_data.db')
cursor = connection.cursor()
# connection.execute(
# '''
# CREATE TABLE hand_annotated(
#     ID INTEGER PRIMARY KEY,
#     quant TEXT,
#     match TEXT,
#     context TEXT,
#     title TEXT,
#     clauses INT,
#     url TEXT,
#     standalone TEXT,
#     processed TEXT,
#     truehit TEXT,
#     truematch TEXT,
#     precedingmodifier TEXT
# )
# ''')

df = pd.read_csv("EXPORT_atc_every_neg_TRUEHITS.csv")

for index, line in df.iterrows():
    print(line)
    cursor.execute('''INSERT INTO hand_annotated VALUES(?,?,?,?,?,?,?,?,?,?)''',
                   (line[0], #ID
                    line[1], #quant,
                    line[11], #match,
                    line[3], #context,
                    line[4],# title,
                    line[5], # clauses,
                    line[6],# url,
                    line[7], #standalone,
                    line[9], #processed,
                    None, #precedingmodifer,
                    ))
    connection.commit()