from flask import Flask, request, jsonify
from flask_cors import CORS
from search_engine import SearchEngine

app = Flask(__name__)
CORS(app)
searchEngine = SearchEngine()


@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Получаем параметр 'str' из запроса
    if not query:
        return jsonify([])
    results = searchEngine.find(query=query)
    return jsonify(results)


# python app.py
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005)
