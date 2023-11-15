import ast
import os
import numpy as np 
import pandas as pd 
import openai 
from openai import OpenAI
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY")
DATA_PATH = "data_processing/full_data.csv"
client = OpenAI()

@st.cache_data(show_spinner=False)
def retrieve_data(): 
    df = pd.read_csv(DATA_PATH)
    df["Embeddings"] = df["Embeddings"].apply(ast.literal_eval)
    return df

@st.cache_data(show_spinner=False)
def get_embedding(search_query): 
    query = search_query.replace("\n", " ")
    return client.embeddings.create(input=[query], model="text-embedding-ada-002").data[0].embedding

@st.cache_data(show_spinner=False)
def get_similarities(search_embedding, df): 
    embeddings = np.array(df["Embeddings"].to_list())
    similarities = np.dot(embeddings, search_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(search_embedding))
    df["Similarities"] = similarities 
    df.sort_values(by="Similarities", ascending=False, inplace=True)
    return df.head(15)

# def main(): 
#     search_query = input("Enter a search query: ")
#     df = retrieve_data()
#     search_embedding = get_embedding(search_query)
#     print(search_embedding)


# if __name__ == "__main__": 
#     main()