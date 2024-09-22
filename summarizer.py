from flask import Flask, request, jsonify
from gensim.summarization import summarize

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def get_summary():
    data = request.get_json()
    text = data['text']
    ratio = float(data.get('ratio', 0.5))  # Ratio of the summarized text length to the original text length

    summary = summarize(text, ratio=ratio)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
