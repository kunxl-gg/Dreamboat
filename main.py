import os
import openai

# importing the env key
api_key = os.getenv("OPENAI_API_KEY")

# fine tun the model
openai.FineTune.create( 
    training_file="data.json",
    model="GPT-3.5-turbo", 
)

# get the completion
completion = openai.ChatCompletion.create( 
    model="GPT-3.5-turbo",
    messages=[ 
    {"role": "system", "content": "You are a chatbot who is good with puns."},
    {"role": "user", "content": ""}
    ]
)

