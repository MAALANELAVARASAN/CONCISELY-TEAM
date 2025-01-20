from flask import Flask, render_template, request, redirect, url_for
from pypdf import PdfReader
import os
from spire.doc import *
from spire.doc.common import *
from spire.presentation import *
from spire.presentation.common import *

app = Flask(__name__)

# Set the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx','pptx'}


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
        
        # Handle PDF files
        if filename.endswith('.pdf'):
            try:
                reader = PdfReader(filename)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return f"File uploaded and extracted successfully: {filename}<br>Extracted Text:<br>{text}"
            except Exception as e:
                return f"Error reading PDF: {str(e)}", 500

        # Handle DOCX files
        elif filename.endswith('.docx'):
            try:
                from docx import Document  # Import here if not at the top
                doc = Document(filename)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return f"File uploaded and extracted successfully: {filename}<br>Extracted Text:<br>{text}"
            except Exception as e:
                return f"Error reading DOCX: {str(e)}", 500
            
        # Handle ppt files 
        elif filename.endswith('.pptx'):
            try:
                presentation = Presentation()
                presentation.LoadFromFile(filename)
                text = []
                for slide in presentation.Slides:
                    for shape in slide.Shapes:
                         if isinstance(shape, IAutoShape):
                             for paragraph in (shape if isinstance(shape, IAutoShape) else None).TextFrame.Paragraphs:
                                 text.append(paragraph.Text)
                output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'ExtractAllText.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    for line in text:
                        f.write(line + '\n')

                presentation.Dispose()
                return f"File uploaded and text extracted successfully: {filename}<br>Extracted Text saved to: {text}"

        

                    
            except Exception as e:
                return f"Error reading PPTX: {str(e)}", 500

                


        # If not a recognized type
        else:
            return f"File uploaded successfully: {filename}"

    return 'Invalid file type', 400

        

if __name__ == '__main__':
    app.run(debug=True)


