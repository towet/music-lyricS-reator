from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Set up Transformers pipeline
generator = pipeline("text-generation", model="gpt2")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate.html", methods=["POST"])
def generate():
    # Get the user's selections from the form
    genre = request.form["genre"]
    verses = int(request.form["verses"])

    # Generate lyrics using Transformers
    prompt = f"{genre} song with {verses} verses about {request.form['topic']}"
    response = generator(prompt, max_length=100, num_return_sequences=1)
    lyrics = response[0]["generated_text"].strip()

    # Organize lyrics by verse
    lines = lyrics.split("\n")
    verses = []
    current_verse = []
    for line in lines:
        if line.startswith("[Verse"):
            if current_verse:
                verses.append(current_verse)
            current_verse = [line]
        else:
            current_verse.append(line)
    if current_verse:
        verses.append(current_verse)

    # Display the generated lyrics on the webpage
    return render_template("generate.html", lyrics=lyrics)

if __name__ == '__main__':
    app.run(debug=True)
