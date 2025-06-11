from flask import Blueprint, request, render_template, current_app
import exifread
import os
from werkzeug.utils import secure_filename

metadata_bp = Blueprint('metadata', __name__, template_folder='templates')

@metadata_bp.route('/', methods=['GET'])
def index():
    return render_template("metadata.html", tags=None)

@metadata_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if not file:
        return "Nessun file caricato.", 400

    # Accesso sicuro alla configurazione da current_app
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        tags = exifread.process_file(f, details=True)

    return render_template("metadata.html", tags=tags if tags else {})
