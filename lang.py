from flask import Flask, render_template_string, request
import asyncio
import inspect
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# HTML Page
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Language Translator</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #6dd5fa, #2980b9);
            color: white;
            text-align: center;
            padding: 50px;
        }
        textarea {
            width: 80%;
            height: 100px;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-size: 16px;
            resize: none;
        }
        select, button {
            padding: 10px;
            margin: 10px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
        }
        button {
            background-color: #2ecc71;
            color: white;
            cursor: pointer;
        }
        .output {
            margin-top: 30px;
            background: white;
            color: black;
            padding: 15px;
            border-radius: 10px;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>
    <h1>🌍 AI Language Translator</h1>
    <form method="POST">
        <textarea name="text" placeholder="Enter text to translate...">{{ text or '' }}</textarea><br>
        <label>Translate To:</label>
        <select name="dest_lang">
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="te">Telugu</option>
            <option value="ta">Tamil</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
        </select><br>
        <button type="submit">Translate</button>
    </form>

    {% if translated_text %}
    <div class="output">
        <h3>Translated Text:</h3>
        <p>{{ translated_text }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def translate_text():
    translated_text = ""
    text = ""
    if request.method == "POST":
        text = request.form["text"]
        dest_lang = request.form["dest_lang"]
        if text:
            try:
                # translator.translate may be a coroutine in some googletrans versions.
                maybe_coro = translator.translate(text, dest=dest_lang)
                if inspect.isawaitable(maybe_coro):
                    result = asyncio.run(maybe_coro)
                else:
                    result = maybe_coro
                translated_text = result.text
            except Exception as e:
                translated_text = "Error: " + str(e)
    return render_template_string(html_code, translated_text=translated_text, text=text)

if __name__ == "__main__":
    app.run(debug=True)
