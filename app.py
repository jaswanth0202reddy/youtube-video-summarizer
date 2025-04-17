from flask import Flask, request, render_template, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization model
summarizer = pipeline("summarization")

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    summary = ""
    
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                # Get video metadata using yt-dlp
                result = subprocess.run([
                    "yt-dlp", 
                    "--get-description", 
                    url
                ], capture_output=True, text=True, check=True)
                
                video_description = result.stdout.strip()
                
                if video_description:
                    # Summarize the description using transformers
                    summary = summarizer(video_description, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                    message = "✅ Summary generated successfully!"
                else:
                    message = "❌ No description found for the video."
                    
            except Exception as e:
                message = f"❌ Error occurred: {str(e)}"
    
    return render_template("index.html", message=message, summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
