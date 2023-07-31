import openai
import os
from openai.embeddings_utils import get_embedding
from typing import List
import pandas as pd


openai.api_key = os.environ.get("OPENAI_API_KEY")
SOURCE_PATH = "src/data_processing/courses.csv"
DATA_PATH = "src/data_processing/full_data.csv"


def get_embeddings(texts) -> List[str]:
    return [get_embedding(text, engine='text-embedding-ada-002') for text in texts]

def write_embeddings_to_file(embeddings, read_path, write_path):
    df = pd.read_csv(read_path)
    df["Embeddings"] = embeddings
    df.to_csv(write_path, index=False)


if __name__ == "__main__": 
    df = pd.read_csv(SOURCE_PATH)
    embeddings = get_embeddings(df["Full Text"].tolist())
    write_embeddings_to_file(embeddings, SOURCE_PATH, DATA_PATH)


