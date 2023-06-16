from flask import Flask, render_template, request
import openai
import os
app = Flask(__name__)

# Set up OpenAI API
openai.api_key = os.environ.get('OPENAI_API_KEY')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate.html", methods=["POST"])
def generate():
    # Get the user's selections from the form
    genre = request.form["genre"]
    verses = int(request.form["verses"])

    # Generate lyrics using OpenAI API
    prompt = f"{genre} song with {verses} verses about {request.form['topic']}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    lyrics = response.choices[0].text.strip()

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)