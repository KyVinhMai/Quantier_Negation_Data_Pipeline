import sqlite3
import whisper
import torch
import torchaudio
from audio_processing.utils import preprocessing_functions as lf
from audio_processing.utils import preprocessing_functions as pf, localization_functions as lf
from force_aligner import force_align

"SQL Database"
conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

"Wav2Vec Model"
torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bundle = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_960HD
model = bundle.get_model().to(device)
labels = bundle.get_labels()

"Whispher Model"
model = whisper.load_model('base')

def extract_match_files(audio_dir: str, utterance:str, transcript, quant:str) -> str:
    "Split audio in half"
    segment = lf.localize_segment(utterance) # Find where in the text the sentence could be
    audio_half = pf.split_audio(audio_dir, segment) # Split audio in half
    audio_half_name, _ = pf.write_audio(audio_half, audio_dir, "halved")  # Put into audio directory
    whisper_transcript = model.transcribe(audio_half_name) # Get transcript

    "Trim audio down to sentence"
    start, end = lf.whisper_time_stamps(utterance, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, audio_half_name)
    trimmed_audio_name, trimmed_path = pf.write_audio(trimmed_audio, audio_dir, "trimmed")

    "Find exact match audio match"
    fa_transcript, index = pf.transform_transcript(utterance, quant)
    word_segments, waveform, trellis = force_align(trimmed_path, fa_transcript, index)
    quant_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    match_audio = lf.extract_sentence(quant_ts, end, trimmed_audio_name)
    _, match_path = pf.write_audio(match_audio, audio_dir, "match")

    match_path = move(match_path)


def main():
    table_data = lf.query_data(cursor)
    for row in table_data:
        #audio_dir, transcript, quant, utterance, context
        audio_dir = row[0]; transcript = row[1], quant = row[2]; utterance = row[3]; context = row[4]
        match_path = extract_match_file()
        context_path = extract_full_file()
