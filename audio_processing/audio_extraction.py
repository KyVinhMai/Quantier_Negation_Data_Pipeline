import sqlite3
import whisper
import torch
import torchaudio
import time
from audio_processing.utils import io_functions as io, minimum_word_distance as md
from audio_processing.utils import preprocessing_functions as pf, localization_functions as lf
from force_aligner import force_align

Audio_folder_path = "E:\\AmbiLab_data\\Audio"

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

"Wav2Vec Model"
torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bundle = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_960H
fa_model = bundle.get_model().to(device)
labels = bundle.get_labels()

"Whisper Model"
model = whisper.load_model('base')

def main():
    table_data = io.query_data(cursor)
    for row in table_data:
        #audio_dir, transcript, quant, utterance, context
        audio_dir = row[0]; json_transcript = row[1], quant = row[2]; utterance = row[3]; context = row[4]
        match_path = extract_match_audio(audio_dir, utterance, json_transcript, quant)
        context_path = extract_full_audio()

        try:
            io.export_Link(cursor, link, audio_dir, clauses, str(transcript.to_json()), 1, str(article_soup))
            conn.commit()
            print("> Exported:", title)
        except sqlite3.Error as er:
            logging.error(
                f"""{'_' * 40}
            Article ~ link db: {title}
            SQL {(' '.join(er.args))}
            {'_' * 40}"""
            )
        num_of_links += 1

        "Export to database"

def extract_match_audio(audio_dir: str, target_utt:str, json_transcript:str, quant:str) -> str:
    "Half Audio -> Trimmed Audio -> Match Audio"
    sentences = pf.load_jsondoc(json_transcript)
    target_utt = pf.rm_nonlexical_items(target_utt)

    "Split audio in half"
    segment = lf.localize_match(sentences, target_utt)  # Find where in the text the sentence could be
    audio_half = pf.split_audio(audio_dir, segment) # Split audio in half
    audio_half_name, _ = io.write_audio(audio_half, audio_dir, "halved")  # Put into audio directory
    whisper_transcript = model.transcribe(audio_half_name) # Get transcript

    "Trim audio down to sentence"
    start, end = md.whisper_time_stamps(target_utt, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, audio_half_name)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, audio_dir, "trimmed")

    "Find exact match audio match"
    fa_transcript, index = pf.insert_vertical(target_utt, quant)
    word_segments, waveform, trellis = force_align(model,device, labels, trimmed_path, fa_transcript)
    quant_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    match_audio = lf.extract_sentence(quant_ts, end, trimmed_audio_name)
    _, match_path = io.write_audio(match_audio, audio_dir, "match")

    match_path = io.move_to_processed_folder(match_path, Audio_folder_path)

    return match_path

def extract_full_audio():
    pass
