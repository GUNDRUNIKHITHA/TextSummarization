from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize
from heapq import nlargest
import nltk

# Download NLTK punkt tokenizer data
nltk.download('punkt')

app = Flask(__name__)

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    word_frequencies = {}
    for sentence in sentences:
        for word in sentence.split():
            word = word.lower()
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    sentence_scores = {}
    for sentence in sentences:
        for word in sentence.split():
            word = word.lower()
            if word in word_frequencies:
                if len(sentence.split()) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    input_text = request.form['input_text']
    input_file = request.files['input_file']
    if input_text:
        summary = summarize_text(input_text)
    elif input_file:
        text = input_file.read().decode('utf-8')
        summary = summarize_text(text)
    else:
        summary = "No input provided"
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
