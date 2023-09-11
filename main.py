import os
import openai
from dotenv import load_dotenv

# loading the env file
load_dotenv()

# importing the env key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# upload the file for fine-tuning
file = openai.File.create(file=open("data.jsonl"), purpose="fine-tune")

print(file)

# # fine-tuning the actual model
model = openai.FineTuningJob.create( 
    training_file=file['id'],
    model ="gpt-3.5-turbo"
)

# waiting for the model to be trained
model = openai.FineTuningJob.retrieve(model['id'])

# printing the model
print(model)

# creating the completion
