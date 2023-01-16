"""
Utilizes partial functions
"""

def export_QuantNeg(cursor, Unique_ID:int, Quant: str, Match:str,
                         Context:str, Title:str, Clauses:int, Link:str, Standalone:int):

    cursor.execute('''INSERT INTO qn_sentences VALUES(?,?,?,?,?,?,?,?)''', (Unique_ID,
                         Quant, Match, Context, Title, Clauses, Link, Standalone))


def export_Link(cursor, Link:str, Audio_dir:str, Clauses:int, Batch, Transcript:str):
    cursor.execute('''INSERT INTO links VALUES(?,?,?,?,?)''', (Link, Audio_dir, Clauses, Batch, Transcript))


def export_Audio(cursor, ID:int, Total_dur:float, match_dur:float,
                      full_dur:float, match_dir:str, full_dir:str, max_pitch:float, min_pitch:float):

    cursor.execute('''INSERT INTO Audio VALUES(?,?,?,?,?,?)''', (ID, Total_dur, match_dur, full_dur,
                         match_dir, full_dir, max_pitch, min_pitch))

def grab_latest_batch():
    pass

def get_last_ID(cursor) -> int:
    "Gets last ID in the list"
    num = cursor.execute('''SELECT * FROM links ORDER BY batches DESC LIMIT 1;''')
    return num
