import os

import whisper

from settings import BASE_DIR

audio_file = str(os.path.join(BASE_DIR, "media", "record.mp3"))

model = whisper.load_model("base")
result = model.transcribe(audio_file)

print(result["text"])