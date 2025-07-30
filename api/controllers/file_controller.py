import os
import pandas as pd
from flask import request
from werkzeug.utils import secure_filename

from api.utils.responses import returnError, returnSuccess
from api.utils.responses import returnError

from api.utils.auth_decorator import token_required

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE_MB = 5

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@token_required
def upload_file():
    if 'file' not in request.files:
        return returnError('No file part in request')

    file = request.files['file']
    if file.filename == '':
        return returnError('No selected file')

    if not allowed_file(file.filename):
        return returnError('Only CSV files are allowed')

    if file.content_length and file.content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        return returnError(f'Max file size is {MAX_FILE_SIZE_MB} MB')

    # Safe filename and path
    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Ensure uploads dir exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(save_path)

    try:
        df = pd.read_csv(save_path, nrows=5) 
        if df.empty or len(df.columns) < 2:
            os.remove(save_path)
            return returnError('CSV must have at least 2 columns and not be empty')
    except Exception as e:
        os.remove(save_path)
        return returnError('Invalid CSV file')

    return returnSuccess('File uploaded and verified', data={'filename': filename})

