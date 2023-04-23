import sqlite3
import whisper
import time
import torch, torchaudio
from audio_processing.utils import io_functions as io, minimum_word_distance as md
from audio_processing.utils import preprocessing_functions as pf, localization_functions as lf
from force_aligner import force_align

Audio_folder_path = "E:\\AmbiLab_data\\Audio"

"Wav2Vec Model"
torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bundle = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_960H
fa_model = bundle.get_model().to(device)
labels = bundle.get_labels()

"Whisper Model"
wh_model = whisper.load_model('base')

def test_splice(audio_dir, json_transcript, quant, utterance, context):
    whisper_transcript, spliced_audio_name = locate_and_splice(
        audio_directory=audio_dir,
        context_target=context,
        json_transcript=json_transcript)

    print(whisper_transcript)


def locate_and_splice(audio_directory:str,
                      context_target:str,
                      json_transcript:str) -> tuple[dict, str]:

    sentences = pf.load_jsondoc(json_transcript)
    target_con = pf.rm_nonlexical_items(context_target)

    "Splice audio"
    context_loc = lf.localize_context(sentences, target_con)  # Find where in the text the sentence could be
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


def extract_context(audio_dir: str, context: str, json_transcript: str) -> str:
    """
    Half Audio -> Trimmed Audio -> Context Audio

    :param audio_dir: path to audio file
    :param context: single string that contains the full context
    :param json_transcript: transcript
    :return: path to processed audio context
    """
    sentences = pf.load_jsondoc(json_transcript)
    context_target = pf.sentencify(context)

    "Split audio in half"
    segment = lf.localize_context(sentences, context_target)
    audio_half = pf.splice_audio(audio_dir, segment)
    audio_half_name, _ = io.write_audio(audio_half, audio_dir, "halved")  # Put into audio directory
    whisper_transcript = wh_model.transcribe(audio_half_name)

    print(whisper_transcript, "\n\n\n", whisper_transcript["segments"])
    "Trim audio down to sentences"
    start, end = md.whisper_context(context_target, whisper_transcript)  # Get time stamps
    # trimmed_audio = lf.extract_sentence(start, end, audio_half_name)
    # trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, audio_dir, "trimmed")



if __name__ == "__main__":
    laptop_audio = "C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\audio_processing\\npr_evictions.mp3"
    laptop_audio2 = "C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\audio_processing\\npr_fiji.mp3"

    utterance = "So eventually, you know, that's where I got. I got to the point that, you know, I realized that everything I was doing was not helping him"; context = ""
    utterance2 = "Financial help is available, but maybe somebody doesn't apply or the assistance never comes through."

    #ID
    context_t = ["CHRISTOPHER-JOYCE: Along the coast of Fiji's big island, Viti Levu, resort hotels and small fishing villages share the same view of the wide, blue Pacific.", 'You will find local musicians in both places.', 'Music is a social lubricate, like the greeting, bula, which can mean many things but mostly everything is just fine.', "But everything isn't just fine.", 'Fijians are noticing changes in their environment.']


    test_splice()

    # extract_match(audio, utterance2, "somebody")
    # extract_context(audio2, "".join(context_t), json_file)