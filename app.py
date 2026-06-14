import os
import re
from flask import Flask, render_template, request, jsonify, send_from_directory
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def create_word_files(text, base_name):
    text_file = f"{base_name}.txt"
    unique_file = f"{base_name}_unique.txt"
    sorted_unique_file = f"{base_name}_sorted_unique.txt"

    text_path = os.path.join(OUTPUT_FOLDER, text_file)
    unique_path = os.path.join(OUTPUT_FOLDER, unique_file)
    sorted_path = os.path.join(OUTPUT_FOLDER, sorted_unique_file)

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    unique_words = set(words)

    with open(unique_path, "w", encoding="utf-8") as f:
        for word in unique_words:
            f.write(word + "\n")

    with open(sorted_path, "w", encoding="utf-8") as f:
        for word in sorted(unique_words):
            f.write(word + "\n")

    return {
        "text_file": text_file,
        "unique_file": unique_file,
        "sorted_unique_file": sorted_unique_file,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("pdfs")

    results = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue

        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(pdf_path)

        text = extract_text(pdf_path)

        base_name = os.path.splitext(filename)[0]

        generated = create_word_files(text, base_name)

        results.append({
            "pdf": filename,
            **generated
        })

    return jsonify(results)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(
        OUTPUT_FOLDER,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
