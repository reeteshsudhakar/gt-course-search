from flask import Flask, jsonify, request
from search.search_functions import (
    retrieve_data,
    get_search_embedding,
    get_similarities,
) 

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    df = retrieve_data()
    search_embedding = get_search_embedding(query)
    results = get_similarities(search_embedding, df)
    return results.to_json(orient="records")


if __name__ == '__main__':
    app.run(debug=True)