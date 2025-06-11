from flask import Flask, render_template
from sentiment.sentiment import sentiment_bp
from metadata.metadata import metadata_bp

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(sentiment_bp, url_prefix="/sentiment")
app.register_blueprint(metadata_bp, url_prefix="/metadata")

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
