import whisper
import torch, torchaudio
import sys
from pathlib import Path
from dataclasses import dataclass
import spacy
nlp = spacy.load('en_core_web_sm')
import time
sys.path.insert(0, r"D:\Research_Projects\Quantifer-Negation\Quantier_Negation_Data_Pipeline")
sys.path.insert(0, r"D:\Research_Projects\Quantifer-Negation\Quantier_Negation_Data_Pipeline\audio_processing")
from audio_processing.utils import io_functions as io, minimum_word_distance as md
from audio_processing.utils import preprocessing_functions as pf, localization_functions as lf
from audio_processing import force_aligner as fa

# from utils import io_functions as io, minimum_word_distance as md
# from utils import preprocessing_functions as pf, localization_functions as lf
# import force_aligner as fa


Audio_folder_path = "D:\Research_Projects\Quantifer-Negation\Quantier_Negation_Data_Pipeline\\audio_processing\\test\\testing_audio_extraction"

"Wav2Vec Model"
torch.random.manual_seed(0)
device = torch.device("cuda") # if torch.cuda.is_available() else "cpu")

bundle = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_960H
fa_model = bundle.get_model().to(device)
labels = bundle.get_labels()

"Whisper Model"
wh_model = whisper.load_model('medium.en')

def test_splice(audio_dir, json_transcript:str, quant, utterance, context):
    whisper_transcript, spliced_audio_name = locate_and_splice(
        audio_directory=audio_dir,
        context_target=context,
        json_transcript=json_transcript)

    print(whisper_transcript, spliced_audio_name)


def locate_and_splice(
        audio_directory: str,
        context_target: list[str],
        json_transcript: str) -> tuple[dict, str]:

    #todo Not happy with preprocessing sentences here.
    #Especially when we're preprocessing only for NPR transcripts
    sentences = pf.load_jsondoc(json_transcript)
    target_con = [pf.rm_nonlexical_items(sent) for sent in context_target]
    audio_len = pf.return_audio_len(audio_directory)# Duration in seconds

    "Splice audio"
    context_location = lf.localize_context(sentences, target_con)  # Find where in the text the sentence could be
    audio_segment = pf.splice_audio(audio_directory, audio_len, context_location)  # Splice audio
    new_audio_name, _ = io.write_audio(audio_segment, audio_directory, "segment")  # Put into audio directory
    whisper_transcript = wh_model.transcribe(new_audio_name)  # Get transcript

    print(f"> Generated {new_audio_name}")

    return whisper_transcript, new_audio_name


def test_match_audio(audio_dir, json_transcript: str, quant, utterance, context):
    whisper_transcript, spliced_audio_name = locate_and_splice(
        audio_directory=audio_dir,
        context_target=context,
        json_transcript=json_transcript)

    match_path = extract_match_audio(
        target_utt=utterance,
        whisper_transcript=whisper_transcript,
        audio_fragment=spliced_audio_name,
        quantifier=quant)

    print(match_path)

def test_context_audio(audio_dir, json_transcript: str, quant, utterance, context):
    whisper_transcript, spliced_audio_name = locate_and_splice(
        audio_directory=audio_dir,
        context_target=context,
        json_transcript=json_transcript)

    match_path = extract_context_audio(
        context_target=context,
        whisper_transcript=whisper_transcript,
        audio_fragment=spliced_audio_name)

    print(match_path)


def extract_match_audio(
        target_utt: str,
        whisper_transcript,
        audio_fragment: str,
        quantifier: str) -> str:

    "Trim audio down to a sentence"
    start, end = md.whisper_time_stamps(target_utt, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, audio_fragment)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, audio_fragment, "trimmed")

    "Find exact match audio match"
    fa_transcript, index = pf.insert_vertical(utterance=target_utt, quant=quantifier)
    word_segments, waveform, trellis = fa.force_align(fa_model, device, labels, trimmed_path, fa_transcript)
    quantifier_ts, _ = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    match_audio = lf.extract_sentence(quantifier_ts, None, trimmed_audio_name)
    _, match_path = io.write_audio(match_audio, audio_fragment, "match")

    match_path = io.move_to_processed_folder(match_path, Audio_folder_path)

    return match_path


def extract_context_audio(audio_fragment, context_target: list[str], whisper_transcript: dict):
    "Trim audio down to sentences"
    start, end = md.whisper_context(context_target, whisper_transcript)  # Get time stamps
    trimmed_audio = lf.extract_sentence(start, end, audio_fragment)
    trimmed_audio_name, trimmed_path = io.write_audio(trimmed_audio, audio_fragment, "trimmed")

    # "Find exact match audio match"
    # fa_transcript = pf.insert_vertical(context="".join(context_target))
    # word_segments, waveform, trellis = fa.force_align(fa_model, device, labels, trimmed_path, fa_transcript)
    # start_ts, end_ts = lf.fa_return_timestamps(waveform, trellis, word_segments, index)
    # match_audio = lf.extract_sentence(start_ts, end_ts, trimmed_audio_name)
    # _, match_path = io.write_audio(match_audio, audio_fragment, "match")
    #
    # context_path = io.move_to_processed_folder(match_path, Audio_folder_path)

    print(trimmed_audio_name, trimmed_path)

@dataclass
class Audio_file:
    audio_path: str
    utterance: str
    transcript: str
    context_t: list[str]
    quant: str

def get_audio_test_data(data_path: Path):
    audio_folders = [f for f in data_path.iterdir() if f.is_dir() and f.name != "processed_audio"]
    unit_test_data = []

    for folder in audio_folders:
        audio_path = [str(f) for f in folder.iterdir() if f.name[-4:] == ".mp3"][0]
        folder_path = str(folder)

        with open(folder_path + "\\utterance.txt", "r") as f:
            utt = f.read()

        with open(folder_path + "\\transcript.txt", "r") as f:
            json_transcript = f.read()

        with open(folder_path + "\\context.txt", "r") as f:
            context = f.read()
            context_t = [i.text for i in nlp(context).sents]

        with open(folder_path + "\\quant.txt", "r") as f:
            quant = f.read()

        data = Audio_file(audio_path,
                   utt,
                   json_transcript,
                   context_t,
                   quant
                   )

        unit_test_data.append(data)

    return unit_test_data


if __name__ == "__main__":
    test1 = False
    test2 = False
    test3 = False
    Automate_test = True

    if test1:
        laptop_audio = "C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\audio_processing\\npr_evictions.mp3"
        utterance = "Financial help is available, but maybe somebody doesn't apply or the assistance never comes through."

    if test2:
        audio_name = "npr_fiji.mp3"
        utterance = "But everything isn't just fine."

        with open("npr_fiji_transcript.txt", "r") as f:
            json_transcript = f.read()

        context_t = [
            "CHRISTOPHER-JOYCE: Along the coast of Fiji's big island, Viti Levu, resort hotels and small fishing villages share the same view of the wide, blue Pacific.",
            'You will find local musicians in both places.',
            'Music is a social lubricate, like the greeting, bula, which can mean many things but mostly everything is just fine.',
            "But everything isn't just fine.", 'Fijians are noticing changes in their environment.']
        quant = "everything"

        test_splice(audio_name, json_transcript, quant, utterance, context_t)

    if test3:
        audio_name = "npr_trayvon_martin.mp3"
        utterance = "everything they have ever done will not become public"

        context_t = ["And this is an unauthorized leak.",
                     "Yes, of course, she\'s right; it\'s unauthorized. ", "It should not have become public. ",
                     "But at this point, is it realistic for anybody in the story - George Zimmerman or Trayvon Martin\'s family - to expect that everything they have ever done will not become public?",
                     "WOODS:Well, that\'s the nature of reporting."]

        with open("npr_trayvon_martin_transcript.txt", "r") as f:
            json_transcript = f.read()

        quant = "everything"
        # test_match_audio(audio_name, json_transcript, quant, utterance, context_t)
        test_context_audio(audio_name, json_transcript, quant, utterance, context_t)

    if Automate_test:
        data = get_audio_test_data(data_path= Path(Audio_folder_path))
        total_time = 0
        for d in data:

            start = time.time()
            test_match_audio(d.audio_path, d.transcript, d.quant, d.utterance, d.context_t)
            end = time.time()
            total_time += end - start

            print(f"{end - start} seconds has elasped")

        print(f"Program took {total_time} to compute.")





    # extract_match(audio, utterance2, "somebody")
    # extract_context(audio2, "".join(context_t), json_file)