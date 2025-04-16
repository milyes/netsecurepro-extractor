from flask import Flask, request, send_from_directory
import os
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "images"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files['pdf']
    if file and file.filename.endswith(".pdf"):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)
        return extract_images(pdf_path)
    return "Format non supporté"

def extract_images(pdf_path):
    doc = fitz.open(pdf_path)
    image_count = 0
    for page_index in range(len(doc)):
        images = doc[page_index].get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            filename = f"image_{page_index+1}_{img_index+1}.{ext}"
            with open(os.path.join(OUTPUT_FOLDER, filename), "wb") as f:
                f.write(image_bytes)
            image_count += 1
    return f"{image_count} image(s) extraite(s)."

@app.route("/")
def index():
    return send_from_directory(".", "extractor.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
