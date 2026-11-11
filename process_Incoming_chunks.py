import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import joblib

#loading the function of create embeddings from read_chunks file
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

#creating a function to use the deepseek model (API) "deepseek-r1 from ollaba library"

def inference(prompt):
    r = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json = {
            "model" : "llama3.2",
            "prompt" : prompt,
            "stream" : False
        }
    )

   
    response = r.json()
    print(f"here is the response : {response}")
    return response

#loading the embeddings again using joblib

df = joblib.load('embeddings.joblib')
df['number'] = df['source_file'].str.split("_").str[0]

incoming_querry = input("Ask a question: ")
question_embedding = create_embedding([incoming_querry])[0]

# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding']).shape)       #these 2 lines are actually showing that the embedding returning  2d vectors (query embedding, other embedding)

#find similarities of question embeddings with other embeddings

similiarities = cosine_similarity(np.vstack(df['embedding'].values), [question_embedding]).flatten()

# print(similiarities)

top_results = 3

max_indx = similiarities.argsort()[::-1][0:top_results]
# print(max_indx)

new_df = df.loc[max_indx]
# print(new_df[["title", "id", "text"]])



#making clean prompt to provide this later to the LLM models....

prompt = f''' I am teaching web development using Sigma web development course. Here are video subtitle 
chunks containing video file, video number, start time in seconds, end time in seconds, text at that time:

{new_df[["title", "number", "text", "start", "end"]].to_json(orient = 'records')}



---------------------------------------------------------------

"{incoming_querry}"
User asked this question related to the video chunks, you have to answer in the human way (do not mention the above format, its just for you to understand) where and how much
content is taught in which video (in which and at what timestamp) and guide the user to go to 
that particular video. If the user asks unrelated question, tell him that you can only answer
questions related to the course
'''
with open("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]
print(f"here is the response : {response}")

with open("response.txt", "w") as f:
    f.write(response)

print(f"the inference for the prompt is : {inference(prompt)}")

# for index, item in new_df.iterrows():
#     print(index, item["title"], item["id"], item["text"], item["start"], item["end"])