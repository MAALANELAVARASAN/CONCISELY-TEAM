from flask import Flask, render_template, request
from pypdf import PdfReader
import os
from spire.doc import *
from spire.presentation import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from docx import Document
from transformers import pipeline
from googletrans import Translator
from deep_translator import GoogleTranslator 
import asyncio 

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Hugging Face T5 model for abstractive summarization
summarizer = pipeline("summarization", model="t5-small")

# Initialize Google Translator
translator = Translator()

def allowed_file(filename):
    """Check if the uploaded file is in the allowed formats."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extractive_summarize(text):
    """Extractive summarization using frequency-based approach."""
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

def abstractive_summarize(text):
    """Abstractive summarization using Hugging Face's T5 model."""
    if len(text.strip()) == 0:
        return "No content to summarize."

    max_input_length = 512  # T5 token limit
    input_text = text[:max_input_length]  # Truncate if too long

    summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def translate_text(text, target_language):
    """Translate text using Google Translate."""
    if target_language == "none":
        return text  # No translation
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    summary_type = request.form.get('summary_type', 'extractive')  # Default to extractive
    target_language = request.form.get('target_language', 'none')  # Default to no translation
    action = request.form.get('action')  # Identify whether to summarize or translate

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        text = ''

        try:
            # Extract text from PDF
            if filename.endswith('.pdf'):
                reader = PdfReader(filename)
                for page in reader.pages:
                    text += page.extract_text()

            # Extract text from DOCX
            elif filename.endswith('.docx'):
                doc = Document(filename)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

            # Extract text from PPTX
            elif filename.endswith('.pptx'):
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

            # Apply selected summarization method
            if summary_type == "abstractive":
                summary = abstractive_summarize(text)
            else:
                summary = extractive_summarize(text)

            # Translate if the user selects the translation option
            if action == "TRANSLATE":
                translated_text = translate_text(text, target_language)
                translated_summary = translate_text(summary, target_language)
                return f"""
                File uploaded successfully: {filename}<br><br>
                Extracted Text:<br>{translated_text}<br><br>
                Translated Summary:<br>{translated_summary}
                """

            return f"""
            File uploaded and extracted successfully: {filename}<br><br>
            Extracted Text:<br>{text}<br><br>
            Summary:<br>{summary}
            """

        except Exception as e:
            return f"Error: {str(e)}", 500

    return 'Invalid file type', 400


async def async_translate(text, target_language):
    """Asynchronous translation function."""
    translated = await translator.translate(text, dest=target_language)
    return translated.text

def translate_text(text, target_language):
    """Wrapper function to handle async translation inside Flask routes."""
    if target_language == "none":
        return text  # No translation needed
    try:
        return asyncio.run(async_translate(text, target_language))
    except Exception as e:
        return f"Translation Error: {str(e)}"


def translate_text(text, target_language):
    """Translate text to the specified language using deep-translator."""
    if target_language == "none" or not text:
        return text  # Return original text if no translation is needed
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        return translator.translate(text)
    except Exception as e:
        return f"Translation Error: {str(e)}"
   

if __name__ == '__main__':
    app.run(debug=True)
    