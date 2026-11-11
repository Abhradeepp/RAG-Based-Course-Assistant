import requests
import os
import json
import pandas as pd
import time
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib


def create_embedding(text_list, batch_size=16):
    all_embeddings = []
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i+batch_size]
        r = requests.post(
            "http://127.0.0.1:11434/api/embed",
            json={"model": "bge-m3", "input": batch},
            timeout=300
        )
        data = r.json()
        if "embeddings" not in data:
            print("ERROR RESPONSE:", data)
            raise RuntimeError(f"Embedding failed on batch {i}-{i+batch_size}")
        all_embeddings.extend(data["embeddings"])
        print(f"  batch {i}-{i+len(batch)} done")
    return all_embeddings


#here we basically checking the chunks that are being processed to the embeddings exist in the
#embeddings.joblib or not , so whenever new audio file along with the json are added newly, the embedding process doesn't to process all the files including
#which are already processed earlier so it will skip and only create embeddings of the newly added chunk(jsons of audios)

if os.path.exists("embeddings.joblib"):
    df = joblib.load("embeddings.joblib")
    already_done = set(df['source_file'])
    chunk_id = df['chunk_id'].max() + 1
    my_dict = df.to_dict('records')
else:
    df = pd.DataFrame()
    already_done = set()
    chunk_id = 0
    my_dict = []

jsons = os.listdir("newjsons") #list all the jsons


for json_file in jsons:

    if json_file in already_done:
        continue


    with open(f"newjsons/{json_file}") as f:
        content = json.load(f)
    print(f"creating embeddings for {json_file}")
    embeddings = create_embedding([c['text'] for c in content['chunks']])
    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embeddings[i]
        chunk['source_file'] = json_file
        chunk_id += 1
        my_dict.append(chunk)
        print(chunk)
     

#creating a pandas data frame of embeddings
df = pd.DataFrame.from_records(my_dict)
#saving this data frame using joblib'
joblib.dump(df, 'embeddings.joblib')


#print(embedding[0:5]) #it will only print 0 - 5 embeddings just for understandings
#a = create_embedding(["I am dynerys Targeryn", "I am a good boy", "i am  a good boy"])
# print(a)