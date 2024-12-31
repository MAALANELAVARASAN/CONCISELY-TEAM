from flask import Flask,render_template,request, redirect, url_for
import os
app=Flask(__name__)

# Set the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 


@app.route('/')
@app.route('/home ')

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
        
        # Ensure the uploads directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(filename)
        return f'File uploaded successfully: {filename}'
    else:
        return 'Invalid file type', 400


@app.route('/about ')
def about():
    return render_template('about.html')


if __name__ == '__main__':   
    app.run(debug=True)

