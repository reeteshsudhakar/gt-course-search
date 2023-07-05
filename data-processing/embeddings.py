import openai
import os
from openai.embeddings_utils import get_embedding
from typing import List
import pandas as pd

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_embeddings(texts) -> List[str]:
    return [get_embedding(text, engine='text-embedding-ada-002') for text in texts]

def write_embeddings_to_file(embeddings, read_path, write_path):
    df = pd.read_csv(read_path)
    df["Embeddings"] = embeddings

    # directory = os.path.dirname(write_path)
    # if not os.path.exists(directory): 
    #     os.makedirs(directory)

    df.to_csv(write_path, index=False)

if __name__ == "__main__": 
    df = pd.read_csv("courses.csv")
    embeddings = get_embeddings(df["Full Text"].tolist())
    write_embeddings_to_file(embeddings, "courses.csv", "full_data.csv")