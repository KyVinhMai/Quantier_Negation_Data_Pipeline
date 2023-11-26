from pathlib import Path
from pydub import AudioSegment
import shutil

# Read and Write functions


def query_data(cursor, show, quant) -> iter:
    table_data = cursor.execute(f'''
    SELECT ID, audio_dir, transcript, utterance, context, links.show, quant
    FROM links INNER JOIN qn_sentences qs
    ON links.link = qs.url
    WHERE links.show LIKE "{show}" AND quant LIKE "%{quant}%"
    ''')
    table_data = iter([line for line in table_data])
    return table_data

def export_Link(cursor, ):
    cursor.execute('''INSERT INTO audio_table VALUES(?,?,?,?,?, ?)''', (Link, Audio_dir, Clauses, Transcript, Batch, html))

def write_audio(audio: AudioSegment, ID:int, folder:str, type:str) -> tuple[str, str]:
    """
    Places new audio in audio directory destination

    returns string title and the directory path to written audio
    """
    assert type in ["segment","trimmed","match", "full"], "Audio type indicator not appropriate"
    # title = audio_dir.split("\\")[-1].split(".")[0] + f"_{type}" + ".wav"

    title = str(ID) + f"_{type}" + ".wav"
    audio_path = folder + "\\" + title
    audio.export(audio_path, format="wav")
    return title, audio_path