from flask import Blueprint, render_template, request
from textblob import TextBlob
from googletrans import Translator

sentiment_bp = Blueprint('sentiment', __name__, template_folder='../templates')

translator = Translator()
variabile_colore = "#00ccff"

def backend(text):
    try:
        type_language = translator.detect(str(text))

        if type_language.lang != "en":
            text_translated = translator.translate(str(text), dest="en")
            text_blob = TextBlob(text_translated.text)
        else:
            text_blob = TextBlob(str(text))

        text_corrected = text_blob.correct()
        sentiment = text_corrected.sentiment.polarity

        if sentiment > 0.5:
            sentimento = "positive"
        elif sentiment > 0:
            sentimento = "neutral"
        else:
            sentimento = "negative"

        return {
            "sentimento": sentimento,
            "lingua": type_language.lang,
            "testo_corretto": text_corrected.string
        }

    except Exception as e:
        return {"errore": str(e)}

@sentiment_bp.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        text = request.form.get("text", "")
        result = backend(text)
    return render_template("sentiment.html", result=result, colore=variabile_colore)
