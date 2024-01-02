import sqlite3
import whisper_timestamped as whisper
import torch
import torchaudio
import os
import string
import logging
from audio_processing.audio_utils import io_functions as io
from audio_processing.audio_utils import minimum_word_distance as md
from audio_processing.audio_utils import localization_functions as lf
from audio_processing.audio_utils import audio_preprocessing_functions as pf
from utils.data_formatting import audio_data_init
from utils.text_preprocessing_functions import sanitize_whisper_transcript
from force_aligner import force_align
import shutil

devices = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
wh_model = whisper.load_model("medium.en", device=devices)

"Logging Configuration"
logging.basicConfig(
    level=logging.INFO,
    filename= "localize_context.log",
    filemode= "w"
)

def main():
    table_data = io.query_hand_annotated_data(cursor, conn, "Fresh Air", "every")
    table_data = [line for line in table_data]

    for row in table_data:
        data = audio_data_init(row)

        print(f"{'='*10} Processing {data.ID} {'='*10}")
        print(f"Utterance: {data.utterance}")
        print(f"Context: {data.context_list}")
        print()

        "Segment Audio -> Trimmed Audio -> Match Audio"

        try:
            whisper_transcript, spliced_audio_dir = locate_and_splice(
                audio_directory=data.audio_dir,
                context_target=data.context_list,
                ID=data.ID,
                folder=data.folder,
                sentences=data.sentences,
                audio_len=data.audio_len
            )

            try:
                match_path = extract_match_audio(
                    ID=data.ID,
                    folder=data.folder,
                    target_utt=data.utterance,
                    whisper_transcript=whisper_transcript,
                    spliced_audio_dir=spliced_audio_dir
                )
            except Exception as e:
                match_path = None
                print(f"ERROR: Issues with obtaining match {e}")

            try:
                context_path = extract_context_audio(
                    ID=data.ID,
                    folder=data.folder,
                    context_target=data.context_str,
                    whisper_transcript=whisper_transcript,
                    spliced_audio_dir=spliced_audio_dir
                )
            except Exception as e:
                context_path = None
                print(f"ERROR: Issues with obtaining context {e} ***")

            if match_path and context_path:
                try:
                    io.export_to_audio(cursor, data.ID, data.audio_len, match_path, context_path, data.audio_dir)
                    conn.commit()
                    io.update_if_processed(cursor, data.ID)
                    print("> Exported:", data.ID)
                except sqlite3.Error as er:
                    print(f"ERROR: Export error {er} ***")

        except Exception as e:
            print(f"ERROR: COULDN'T GRAB AUDIO")

        "Copy entire audio to folder"
        shutil.copy(data.audio_dir, data.folder)
        with open(f"{data.folder}\\{data.ID}_transcript.txt", "w", encoding="utf-8") as f:
            f.write(data.sentences)


def cleanup(folder, ID):
    segfile = folder + f"\\{ID}_segment.wav"
    if os.path.isfile(segfile):
        os.remove(segfile)
    else:
        print("Error: %s file not found" % segfile)

    trimfile = folder + f"\\{ID}_trimmed.wav"
    if os.path.isfile(trimfile):
        os.remove(trimfile)
    else:
        print("Error: %s file not found" % trimfile)

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
    _, spliced_audio_dir = io.write_audio(audio_segment, ID, folder, "segment"); print("+ Generating Whisper Transcript +")  # Put into audio directory

    audio = whisper.load_audio(spliced_audio_dir)

    whisper_transcript = whisper.transcribe(wh_model, audio, language="en")  # Get transcript

    return whisper_transcript, spliced_audio_dir

def extract_match_audio(ID: int,
                        folder: str,
                        target_utt: str,
                        whisper_transcript,
                        spliced_audio_dir:str
                        ) -> str:

    "Trim audio down to sentence"
    transcript = sanitize_whisper_transcript(whisper_transcript)
    target_utt = target_utt.translate(str.maketrans('', '', string.punctuation))

    start, end, _ = md.whisper_time_stamps(target_utt, transcript)  # Get time stamps

    end += 300  #TODO change this hardcoding

    trimmed_audio = lf.extract_sentence(start, end, spliced_audio_dir)
    _, trimmed_path = io.write_audio(trimmed_audio, ID, folder, "match_trimmed")

    "Find exact match audio match"
    fa_transcript = pf.insert_vertical(target_utt)
    word_segments, waveform, trellis = force_align(fa_model, device, labels, trimmed_path, fa_transcript)
    quant_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments)
    match_audio = lf.extract_sentence(quant_ts, end, trimmed_path)
    _, match_path = io.write_audio(match_audio,  ID, folder, "match")


    print("<< Extracted Match File! >>")

    return match_path

def extract_context_audio(ID: int,
                        folder: str,
                        context_target: str,
                        whisper_transcript,
                        spliced_audio_dir:str
):

    start, end, _ = md.whisper_time_stamps(context_target, whisper_transcript)

    start -= 500
    end += 500

    trimmed_audio = lf.extract_sentence(start, end, spliced_audio_dir)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, ID, folder, "full")

    print("<< Extracted Context File! >>")

    return trimmed_path

if __name__ == '__main__':
    dict = {
        0: ("All Things Considered", "every"),
        1: ("All Things Considered", "all")
    }
    main()
