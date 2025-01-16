from flask import Flask, render_template, request, redirect, url_for
from pypdf import PdfReader
import os
import docx
from docx import Document

app = Flask(__name__)

# Set the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        
        # Extract text from PDF
        if filename.endswith('.pdf'):
            try:
                reader = PdfReader(filename)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return f"File uploaded and extracted successfully: {filename}<br>Extracted Text:<br>{text}"
            except Exception as e:
                return f"Error reading PDF: {str(e)}", 500
        else:
            return f"File uploaded successfully: {filename}"
    else:
        return 'Invalid file type', 400

   

# Create a new Word document
        doc = Document()
        doc.add_heading('Sample Title', level=1)
        doc.add_paragraph('This is a paragraph in the Word document.')

# Save the document
        doc.save('sample.docx')
    

        





@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)