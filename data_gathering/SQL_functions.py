"""
Utilizes partial functions
"""

def export_QuantNeg(cursor, Unique_ID:int, Quant: str, Match:str,
                         Context:str, Title:str, Clauses:int, Link:str, Standalone:int, Utterance:str, show:str):

    cursor.execute('''INSERT INTO qn_sentences VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (Unique_ID,
                         Quant, Match, Context, Title, Clauses, Link, Standalone, Utterance,"No", show))


def export_Link(cursor, Link:str, Audio_dir:str, Clauses:int, Transcript:str, Batch:int, html:str, show_title: str):
    cursor.execute('''INSERT INTO links VALUES(?,?,?,?,?,?,?)''',
                   (Link,
                    Audio_dir,
                    Clauses,
                    Transcript,
                    Batch,
                    html,
                    show_title))


def export_Audio(cursor, ID:int, Total_dur:float, match_dur:float,
                      full_dur:float, match_dir:str, full_dir:str, max_pitch:float, min_pitch:float):

    cursor.execute('''INSERT INTO Audio VALUES(?,?,?,?,?,?)''',
                   (ID,
                    Total_dur,
                    match_dur,
                    full_dur,
                    match_dir,
                    full_dir,
                    max_pitch,
                    min_pitch))

def grab_latest_batch(cursor):
    num = cursor.execute('''SELECT * FROM links ORDER BY batches DESC LIMIT 1;''')
    return num

def QN_last_ID(cursor) -> int:
    "Gets last ID in the table"
    cursor.execute('''SELECT id FROM qn_sentences ORDER BY id DESC LIMIT 1;''')
    ID = cursor.fetchone()
    return 440 if ID is None else ID[0]

def select_batch(cursor, conn, show:str) -> iter:
    data_iter = cursor.execute(f"SELECT * FROM links WHERE show like '%{show}%';")
    conn.commit()
    return data_iter
