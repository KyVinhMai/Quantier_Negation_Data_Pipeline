from pydub import AudioSegment
# Read and Write functions


def query_qn_sentences_data(cursor, show, quant) -> iter:
    table_data = cursor.execute(f'''
    SELECT ID, audio_dir, transcript, utterance, context, links.show, quant
    FROM links INNER JOIN qn_sentences qs
    ON links.link = qs.url
    WHERE links.show LIKE "{show}" AND quant LIKE "%{quant}%"
    ''')
    table_data = iter([line for line in table_data])
    return table_data

def query_hand_annotated_data(cursor, conn, show, quant) -> iter:
    table_data = cursor.execute(f'''
    SELECT ID, audio_dir, transcript, match, context, links.show, quant
    FROM links INNER JOIN hand_annotated ha
    ON links.link = ha.url
    WHERE links.show LIKE "{show}" AND quant LIKE "%{quant}%"
    ''')
    conn.commit()
    return table_data

def export_to_audio(cursor, ID: int, audio_len: float, match_path: str, context_path: str, original_path: str):
    cursor.execute('''INSERT INTO audio_table VALUES(?,?,?,?,?)''', ( ID, audio_len, match_path, context_path, original_path))

def write_audio(audio: AudioSegment, ID:int, folder:str, type:str) -> tuple[str, str]:
    """
    Places new audio in audio directory destination

    returns string title and the directory path to written audio
    """
    assert type in ["segment","match_trimmed","match","full"], "Audio type indicator not appropriate"

    title = str(ID) + f"_{type}" + ".wav"
    audio_path = folder + "\\" + title
    audio = audio.set_channels(1) # Turn into mono
    audio.export(audio_path, format="wav")
    print(f" > Created {audio_path}")
    return title, audio_path

def update_if_processed(cursor, num:int):
    cursor.execute(f'''UPDATE hand_annotated SET processed = "yes" WHERE ID = {num}''')
