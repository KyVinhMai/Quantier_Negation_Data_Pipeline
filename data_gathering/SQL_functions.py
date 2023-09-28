"""
Utilizes partial functions
"""

def export_QuantNeg(cursor, Unique_ID:int, Quant: str, Match:str,
                         Context:str, Title:str, Clauses:int, Link:str, Standalone:int, Utterance:str):

    cursor.execute('''INSERT INTO qn_sentences VALUES(?,?,?,?,?,?,?,?,?,?)''', (Unique_ID,
                         Quant, Match, Context, Title, Clauses, Link, Standalone, Utterance,"No"))


def export_Link(cursor, Link:str, Audio_dir:str, Clauses:int, Transcript:str, Batch:int, html:str):
    cursor.execute('''INSERT INTO links VALUES(?,?,?,?,?, ?)''', (Link, Audio_dir, Clauses, Transcript, Batch, html))


def export_Audio(cursor, ID:int, Total_dur:float, match_dur:float,
                      full_dur:float, match_dir:str, full_dir:str, max_pitch:float, min_pitch:float):

    cursor.execute('''INSERT INTO Audio VALUES(?,?,?,?,?,?)''', (ID, Total_dur, match_dur, full_dur,
                         match_dir, full_dir, max_pitch, min_pitch))

def grab_latest_batch(cursor):
    num = cursor.execute('''SELECT * FROM links ORDER BY batches DESC LIMIT 1;''')
    return num

def QN_last_ID(cursor) -> tuple:
    "Gets last ID in the table"
    cursor.execute('''SELECT id FROM qn_sentences ORDER BY id DESC LIMIT 1;''')
    return cursor.fetchone()

def select_batch(cursor, conn, batch_num:str) -> iter:
    data_iter = cursor.execute('''SELECT * FROM links WHERE batches = 2;''') #todo remove unnecessaray columns
    conn.commit()
    return data_iter

