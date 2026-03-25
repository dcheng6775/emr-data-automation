from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from utils import extract_text, extract_data
import csv
import io

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    texts = []
    for i in range(1, 4):
        uploaded_file = request.files.get(f"file{i}")
        if uploaded_file and uploaded_file.filename:
            text = extract_text(uploaded_file)
            texts.append(text)

    if not texts:
        return jsonify({"error": "No files received"}), 400

    full_text = "\n".join(texts)
    results = extract_data(full_text)
    return jsonify(results)

@app.route("/export", methods=["POST"])
def export():
    texts = []
    for i in range(1, 4):
        uploaded_file = request.files.get(f"file{i}")
        if uploaded_file and uploaded_file.filename:
            text = extract_text(uploaded_file)
            texts.append(text)

    if not texts:
        return jsonify({"error": "No files received"}), 400

    full_text = "\n".join(texts)
    results = extract_data(full_text)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(results.keys())
    writer.writerow(results.values())

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=emr_results.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)