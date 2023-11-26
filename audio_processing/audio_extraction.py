import sqlite3
import whisper
import torch
import torchaudio
import time
from audio_processing.utils import io_functions as io
from audio_processing.utils import minimum_word_distance as md
from audio_processing.utils import localization_functions as lf
from audio_processing.utils import audio_preprocessing_functions as pf
from utils.data_formatting import audio_data_init
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
wh_model = whisper.load_model('base')

"Timing Information"
times = []

def main():
    table_data = io.query_data(cursor)
    for row in table_data:
        data = audio_data_init(row)

        "Segment Audio -> Trimmed Audio -> Match Audio"
        whisper_transcript, spliced_audio_name = locate_and_splice(
            audio_directory=data.audio_dir,
            context_target=data.context,
            ID=data.ID,
            folder=data.folder,
            sentences=data.sentences,
            audio_len=data.audio_len
        )

        match_path = extract_match_audio(
            ID=data.ID,
            folder=data.folder,
            target_utt=data.utterance,
            whisper_transcript=whisper_transcript,
            spliced_audio_name=spliced_audio_name,
            quantifier=data.quant
        )

        context_path = extract_context_audio()

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


def locate_and_splice(
        audio_directory: str,
        context_target: list[str],
        ID: int,
        folder: str,
        sentences: list[str],
        audio_len: float) -> tuple[dict, str]:

    "Splice audio"
    context_loc = lf.localize_context(sentences, context_target)  # Finds where in the text the sentence could be
    audio_segment = pf.splice_audio(audio_directory, audio_len, context_loc)  # Splice audio
    spliced_audio_name, _ = io.write_audio(audio_segment, ID, folder, "segment")  # Put into audio directory
    whisper_transcript = wh_model.transcribe(spliced_audio_name)  # Get transcript

    return whisper_transcript, spliced_audio_name

def extract_match_audio(ID: int,
                        folder: str,
                        target_utt:str,
                        whisper_transcript,
                        spliced_audio_name:str,
                        quantifier:str) -> str:

    "Trim audio down to sentence"
    start, end = md.whisper_time_stamps(target_utt, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, spliced_audio_name)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, ID, folder, "trimmed")

    "Find exact match audio match"
    fa_transcript, index = pf.insert_vertical(target_utt, quantifier)
    word_segments, waveform, trellis = force_align(fa_model, device, labels, trimmed_path, fa_transcript)
    quant_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    match_audio = lf.extract_sentence(quant_ts, end, trimmed_audio_name)
    _, match_path = io.write_audio(match_audio,  ID, folder, "match")

    return match_path

def extract_context_audio(
        context_target: list[str],
        whisper_transcript: dict,
        spliced_audio_name:str,
):
    start, _ = md.whisper_time_stamps(context_target[0], whisper_transcript)
    _, end = md.whisper_time_stamps(context_target[-1], whisper_transcript)


if __name__ == '__main__':
    dict = {
        0: ("All Things Considered", "every"),
        1: ("All Things Considered", "all")
    }
    pass
