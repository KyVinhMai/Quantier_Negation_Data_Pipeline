import whisper_timestamped as whisper
import json
import torch

devices = torch.device("cuda" if torch.cuda.is_available() else "cpu")

audio = whisper.load_audio("npr_evictions.mp3")

model = whisper.load_model("medium.en", device=devices)

result = whisper.transcribe(model, audio, language="fr")

print(json.dumps(result, indent = 2, ensure_ascii = False))