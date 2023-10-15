import sqlite3
import whisper
import torch
import torchaudio
import time
from audio_processing.utils import io_functions as io, minimum_word_distance as md
from audio_processing.utils import audio_preprocessing_functions as pf, localization_functions as lf
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

def main():
    table_data = io.query_data(cursor)
    for row in table_data:
        #audio_dir, transcript, quant, utterance, context
        audio_dir = row[0]; json_transcript = row[1], quant = row[2]; utterance = row[3]; context = row[4]

        "Segment Audio -> Trimmed Audio -> Match Audio"
        whisper_transcript, spliced_audio_name = locate_and_splice(
            audio_directory=audio_dir,
            context_target=context,
            json_transcript=json_transcript)

        match_path = extract_match_audio(
            audio_directory=audio_dir,
            target_utt=utterance,
            whisper_transcript=whisper_transcript,
            spliced_audio_name=spliced_audio_name,
            quantifier=quant)

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


def locate_and_splice(audio_directory:str,
                      context_target:str,
                      json_transcript:str) -> tuple[dict, str]:

    sentences = pf.load_jsondoc(json_transcript)
    target_con = pf.rm_nonlexical_items(context_target)

    "Splice audio"
    context_loc = lf.localize_context(sentences, target_con)  # Finds where in the text the sentence could be
    audio_segment = pf.splice_audio(audio_directory, context_loc)  # Splice audio
    spliced_audio_name, _ = io.write_audio(audio_segment, audio_directory, "segment")  # Put into audio directory
    whisper_transcript = wh_model.transcribe(spliced_audio_name)  # Get transcript

    return whisper_transcript, spliced_audio_name

def extract_match_audio(audio_directory: str, target_utt:str,
                        whisper_transcript,
                        spliced_audio_name:str,
                        quantifier:str) -> str:

    "Trim audio down to sentence"
    start, end = md.whisper_time_stamps(target_utt, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, spliced_audio_name)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, audio_directory, "trimmed")

    "Find exact match audio match"
    fa_transcript, index = pf.insert_vertical(target_utt, quantifier)
    word_segments, waveform, trellis = force_align(fa_model, device, labels, trimmed_path, fa_transcript)
    quant_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    match_audio = lf.extract_sentence(quant_ts, end, trimmed_audio_name)
    _, match_path = io.write_audio(match_audio, audio_directory, "match")

    match_path = io.move_to_processed_folder(match_path, Audio_folder_path)

    return match_path

def extract_context_audio():
    pass
