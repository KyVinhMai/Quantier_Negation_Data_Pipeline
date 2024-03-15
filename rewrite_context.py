import pandas as pd
import sqlite3
from utils.text_preprocessing_functions import load_json
from quant_neg_detection.QNI import get_context

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

df = pd.read_csv("allthingsconsidered_all_neg_handAnnotated.csv", encoding='latin-1')

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

        transcript = load_json(transcript_data[0], include_speaker_info=True)

        for index, sent in enumerate(transcript):
            if match in sent:
                indices = [index]
                df.at[row_index, "full_transcript"] = get_context(transcript, indices, num_before=3, num_after=2)
                df.at[row_index, "long_transcript"] = get_context(transcript, indices, num_before=4, num_after=3)
                df.at[row_index, "xlong_transcript"] = get_context(transcript, indices, num_before=8, num_after=5)


df.to_csv("3context_Allneg_AllThingsConsidered_handannotated.csv", index=False)
