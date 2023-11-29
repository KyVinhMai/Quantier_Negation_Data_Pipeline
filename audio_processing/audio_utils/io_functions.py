from pathlib import Path
from pydub import AudioSegment
import shutil

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

def export_Link(cursor, ):
    cursor.execute('''INSERT INTO audio_table VALUES(?,?,?,?,?, ?)''', (Link, Audio_dir, Clauses, Transcript, Batch, html))

def write_audio(audio: AudioSegment, ID:int, folder:str, type:str) -> tuple[str, str]:
    """
    Places new audio in audio directory destination

    returns string title and the directory path to written audio
    """
    assert type in ["segment","trimmed","match", "full"], "Audio type indicator not appropriate"

    title = str(ID) + f"_{type}" + ".wav"
    audio_path = folder + "\\" + title
    audio.export(audio_path, format="wav")
    print(f" > Created {audio_path}")
    return title, audio_path