from pathlib import Path
from pydub import AudioSegment
import shutil

# Read and Write functions


def query_data(cursor) -> iter:
    table_data = cursor.execute('''SELECT transcript, utterance, context FROM links INNER JOIN qn_sentences qs ON links.link = qs.url;''')
    table_data = iter([line for line in table_data])
    return table_data

def export_Link(cursor, ):
    cursor.execute('''INSERT INTO audio_table VALUES(?,?,?,?,?, ?)''', (Link, Audio_dir, Clauses, Transcript, Batch, html))

def write_audio(audio: AudioSegment, audio_dir:str, type:str) -> tuple[str, str]:
    """
    Places new audio in audio directory destination

    returns string title and the directory path to written audio
    """
    assert type in ["segment","trimmed","match"], "Audio type indicator not appropriate"
    title = audio_dir.split("\\")[-1].split(".")[0] + f"_{type}" + ".wav"
    audio.export(title, format="wav")
    trimmed_audio_path = str(Path.cwd()) + '\\' + title
    return title, trimmed_audio_path

def move_to_processed_folder(audio_path, destination_path) -> str:
    "Moves audio to processed subfolder"
    new_destination = destination_path + "\\processed_audio"
    shutil.move(audio_path, new_destination)
    return new_destination