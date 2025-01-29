from flask import Flask, render_template, request
from pypdf import PdfReader
import os
from spire.doc import *
from spire.presentation import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from docx import Document

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def summarize_text(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    freq_table = {}
    for word in words:
        word = word.lower()
        if word not in stop_words:
            freq_table[word] = freq_table.get(word, 0) + 1
    
    sentences = sent_tokenize(text)
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq_table:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq_table[word]
    
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:5]
    return ' '.join(summary_sentences)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        text = ''
        #handles pdf file
        if filename.endswith('.pdf'):
            try:
                reader = PdfReader(filename)
                for page in reader.pages:
                    text += page.extract_text()
            except Exception as e:
                return f"Error reading PDF: {str(e)}", 500
        #handles word file
        elif filename.endswith('.docx'):
            try:
                doc = Document(filename)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            except Exception as e:
                return f"Error reading DOCX: {str(e)}", 500
        #handles ppt file 
        elif filename.endswith('.pptx'):
            try:
                presentation = Presentation()
                presentation.LoadFromFile(filename)
                text = []
                for slide in presentation.Slides:
                    for shape in slide.Shapes:
                        if isinstance(shape, IAutoShape):
                            for paragraph in shape.TextFrame.Paragraphs:
                                text.append(paragraph.Text)
                text = '\n'.join(text)
                presentation.Dispose()
            except Exception as e:
                return f"Error reading PPTX: {str(e)}", 500

        summary = summarize_text(text)
        return f"File uploaded and extracted successfully: {filename}<br><br>Extracted Text:<br>{text}<br><br>Summary:<br>{summary}"
    
    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=True)
