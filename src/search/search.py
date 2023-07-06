import ast
import os
import numpy as np 
import pandas as pd 
import openai 
from openai.embeddings_utils import get_embedding

openai.api_key = os.getenv("OPENAI_API_KEY")
DATA_PATH = "src/data_processing/full_data.csv"

def retrieve_data(): 
    df = pd.read_csv(DATA_PATH)
    df["Embeddings"] = df["Embeddings"].apply(ast.literal_eval)
    return df

def get_search_embedding(search_query): 
    search_embedding = get_embedding(search_query, engine="text-embedding-ada-002")
    return search_embedding 

def get_similarities(search_embedding, df): 
    embeddings = np.array(df["Embeddings"].to_list())
    similarities = np.dot(embeddings, search_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(search_embedding))
    df["Similarities"] = similarities 
    df.sort_values(by="Similarities", ascending=False, inplace=True)
    return df.head(15)

def main(): 
    search_query = input("Enter a search query: ")
    df = retrieve_data()
    search_embedding = get_search_embedding(search_query)
    results = get_similarities(search_embedding, df)
    print(results)


if __name__ == "__main__": 
    main()