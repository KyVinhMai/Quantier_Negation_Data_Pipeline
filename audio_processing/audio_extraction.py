import whisper
from localization_functions import localize_segment

#Run on NULL items


model = whisper.load_model()

audio = whisper.load_audio()
audio = whisper.pad_or_trim(audio) # will fit 30 second intervals

mel = whisper.log_mel_spectogram(audio).to(model.device)
_, probs = model.detect_language(mel)

print(f"Detected language: {max(probs, key=probs.get)}")

options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

print(result.text)