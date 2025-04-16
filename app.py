import os
from flask import Flask, request, render_template, send_from_directory
from pdf2image import convert_from_path
from pathlib import Path
from ia_logic import analyze_image

app = Flask(__name__)

def extract_images(pdf_path, output_dir="static/output_images", dpi=300):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    analyses = []

    images = convert_from_path(str(pdf_path), dpi=dpi)
    for i, img in enumerate(images):
        output_file = output_dir / f"page_{i+1:03}.png"
        img.save(output_file, "PNG")
        result = analyze_image(output_file)
        analyses.append({"image": output_file.name, "result": result})

    return len(images), analyses

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        if pdf_file:
            uploads_dir = Path("uploads")
            uploads_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = uploads_dir / pdf_file.filename
            pdf_file.save(pdf_path)
            num_images, analyses = extract_images(pdf_path)
            return render_template('results.html', num_images=num_images, pdf_filename=pdf_file.filename, analyses=analyses)
    return render_template('index.html')

@app.route('/output_images/<path:filename>')
def send_image(filename):
    return send_from_directory('static/output_images', filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('uploads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
