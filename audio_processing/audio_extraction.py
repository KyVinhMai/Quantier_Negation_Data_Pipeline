import sqlite3
import whisper
import pydub
import preprocessing_functions as lf
conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()
model = whisper.load_model('base')

#Trimming
def main():
    table_data = lf.query_data(cursor)
    for row in table_data:
        audio_dir = row[1]; utterance = row[2]; context = row[3]
        segment = lf.localize_segment(row, utterance)
        trimmed_audio = lf.split_audio(audio_dir, segment)
        trim_file_name = lf.write_audio(trimmed_audio, audio_dir)

        audio = whisper.load_audio(trim_file_name)
        audio = whisper.pad_or_trim(audio) # will fit 30 second intervals

        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)

        print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions(fp16 = False)
        result = whisper.decode(model, mel, options)

        print(result.text)
