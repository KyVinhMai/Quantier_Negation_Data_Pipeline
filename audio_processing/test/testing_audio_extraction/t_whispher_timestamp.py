import whisper_timestamped as whisper
import json
import torch

devices = torch.device("cuda" if torch.cuda.is_available() else "cpu")

audio = whisper.load_audio("npr_trayvon_martin.mp3")

model = whisper.load_model("medium.en", device=devices)

result = whisper.transcribe(model, audio, language="en")

with open("../test_helper_functions/npr_trayvon_martin_transcript.json", "w") as outfile:
    json.dump(result, outfile, indent=2, ensure_ascii = False)

print(json.dumps(result, indent = 2, ensure_ascii = False))