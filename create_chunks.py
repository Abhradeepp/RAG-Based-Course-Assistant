import whisper
import os
import json

model = whisper.load_model("medium")

audios = os.listdir("audios")

for audio in audios:
    number = audio.split("_")[0]
    title = audio.split("_")[1][:-4]

    output_path = f"jsons/{audio}.json"
    print("Checking:", repr(output_path), "Exists:", os.path.exists(output_path)) #just for checking whether the files are already processed or not
    if os.path.exists(output_path):
        continue

    print(number, title)
    result = model.transcribe(audio = f"audios/{audio}",
                              language = "hi",
                              task = "translate",
                              word_timestamps= False)
    chunks = []
    for id, segment in enumerate(result["segments"]):
        chunks.append({
        "id": id,
        "title": title,
        "start": segment["start"],
        "end": segment["end"],
        "text": segment["text"]
        })

    chunks_with_metadata = {"chunks" : chunks, "text" : result["text"]}

    with open(f"jsons/{audio}.json", "w") as f:
        json.dump(chunks_with_metadata, f)
