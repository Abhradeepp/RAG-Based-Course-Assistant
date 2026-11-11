How the pipeline is working

##step 1
Load the videos to the file that you want

##step 2
run the "process_videos.py" file to convert all those mp4s to mp3

##step 3

now its time to create chunks from all the respective audios
that means we need create a json file where every chunks will be processed and for that we need to use
a specific model of Whisper (using medium) because of gpu issues

--- run the "create_chunks.py" to convert those mp3 s to the chunks into json file

##step 4

chunks has been created now we need to make embeddings(vectors) so that machine can maths the vectors 
in a 2d manner whenever incoming querry is given

---run "read_chunks.py" inorder to convert the json chunks to the embeddings

##step 5

Okay ! so far so good , but now we also have to make the embeddings of the incoming querry
and also we need to make a prompt which can be given to the model so that it can answer
for now we are using LLM model - llama3.2 pretty decent model but not that accurate enough to work with
but gets the job done anyhow

---run "process_incoming_chunks.py" inorder to convert the incoming querry to embeddings and create prompt

##step 6

This is a little improvement we have done with the making of chunks,
the chunks are so tiny that when it is passed to the llma it becomes so confusing for the model
rather we created a new python program which retrives json files from "jsons" and make a merge of 5 consecutive chunks
so that we can reduce the number of chunks per audio as well as increase the number of texts in per chunks

---run "merge_chunks.py" inorder to merge the 5 chunks in to 1