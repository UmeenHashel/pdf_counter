from flask import Flask, request, jsonify, send_from_directory
import fitz  # PyMuPDF
from docx import Document
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def count_pdf_pages(file_path):
    pdf_document = fitz.open(file_path)
    return pdf_document.page_count

def count_docx_pages(file_path):
    doc = Document(file_path)
    # Simple page count estimation based on the number of paragraphs (this is not accurate)
    # You might need a more sophisticated approach for accurate page count
    return len(doc.paragraphs) // 10

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/scripts/<path:path>')
def send_scripts(path):
    return send_from_directory('scripts', path)

@app.route('/styles/<path:path>')
def send_styles(path):
    return send_from_directory('styles', path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        if file.filename.endswith('.pdf'):
            page_count = count_pdf_pages(file_path)
        else:
            page_count = count_docx_pages(file_path)

        return jsonify({'pageCount': page_count})
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
