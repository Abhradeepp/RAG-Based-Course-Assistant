import os
import json
import math

n = 5 #no of chunks we want to merge into 1 chunk

for file_name in os.listdir("jsons"):
    if file_name.endswith("json"):
        file_path = os.path.join("jsons", file_name) 
        with open(file_path, "r", encoding = "utf-8") as f:
            data = json.load(f)
            new_chunks = []
            num_chunks = len(data['chunks'])
            num_groups = math.ceil(num_chunks/n)

            for i in range(num_groups):
                start_idx = i*n
                end_indx = min((i+1)*n, num_chunks)
                # now grouping the chunks from start index to the end index
                chunk_group = data['chunks'][start_idx: end_indx]

                #creating new chunks and appending datas which we require
                new_chunks.append({
                    "id" : data['chunks'][0]['id'],
                    "title": chunk_group[0]['title'],
                    "start" : chunk_group[0]['start'],
                    "end" : chunk_group[-1]['end'],
                    "text" : " ".join(c['text'] for c in chunk_group)
                })

                #save file without double .json
                os.makedirs("newjsons", exist_ok=True)
                with open(os.path.join("newjsons", file_name), "w", encoding="utf-8") as json_file:
                    json.dump({"chunks" : new_chunks, "text" : data['text']}, json_file, indent = 4)
