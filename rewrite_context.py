import pandas as pd
import sqlite3
from utils.text_preprocessing_functions import load_json
from quant_neg_detection.QNI import get_context

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

df = pd.read_csv("every_neg_Fresh_Air_handAnnotated.csv", encoding='latin-1')

if __name__ == "__main__":
    for row_index, row in df.iterrows():
        match = row[2]
        url = row[6]

        transcript_data = [row for row in cursor.execute(f'''
            SELECT transcript
            FROM links 
            WHERE links.link LIKE "{url}"
            ''')][0]
        conn.commit()

        transcript = load_json(transcript_data[0])

        for index, sent in enumerate(transcript):
            if match in sent:
                indices = [index]
                new_context = get_context(transcript, indices)
                df.at[row_index, "context"] = new_context

df.to_csv("new_Fresh_Air_everyneg_handannotated.csv", index=False)
