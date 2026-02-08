from flask import Flask, request, render_template
from utils import *
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    table_html = None
    
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
        
        if texts:
            full_text = "\n".join(texts)
            results = extract_data(full_text)
            
            if results:
                df = pd.DataFrame([results])
                table_html = df.to_html(classes='table table-striped', index=False)
        
    return render_template("index.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)