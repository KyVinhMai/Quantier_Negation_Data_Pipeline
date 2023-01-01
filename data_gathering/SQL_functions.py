"""
Utilizes partial functions
"""

def export_QuantNeg(cursor, Unique_ID:int, Title:str, Quant: str, Match:str,
                         Context:str, Link:str, Clauses:int, Date:str, Standalone:str):

    cursor.execute('''INSERT INTO QuantNeg VALUES(?,?,?,?,?,?,?,?)''', (Unique_ID, Title,
                         Quant, Match, Context, Link, Clauses, Date, Standalone))


def export_Link(cursor, Link:int, Show_type:str,
                         Transcript:str, Audio_dir:str, Audio_link:str, Clauses:int):

    cursor.execute('''INSERT INTO Links VALUES(?,?,?,?,?,?)''', (Link, Show_type,
                         Transcript, Audio_dir, Audio_link, Clauses))


def export_Audio(cursor, ID:int, Total_dur:float, match_dur:float,
                      full_dur:float, match_dir:str, full_dir:str, max_pitch:float, min_pitch:float):

    cursor.execute('''INSERT INTO Audio VALUES(?,?,?,?,?,?)''', (ID, Total_dur, match_dur, full_dur,
                         match_dir, full_dir, max_pitch, min_pitch))


def get_last_ID(cursor) -> int:
    "Gets last ID in the list"
    num = cursor.execute('''SELECT from *  QuantNeg ''')
    return num
