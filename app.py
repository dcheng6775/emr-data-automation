from flask import Flask, request, render_template
from utils import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        texts = []
        for i in range(1, 4):
            uploaded_file = request.files.get(f"file{i}")
            text_input = request.form.get(f"text{i}")

            if uploaded_file and uploaded_file.filename:
                text = extract_text(uploaded_file)
                texts.append(text)
            elif text_input:
                texts.append(text_input)
        full_text = "\n".join(texts)
        results = extract_data(full_text)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)