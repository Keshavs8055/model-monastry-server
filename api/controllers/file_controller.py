import os
import pandas as pd
from flask import request, g
from werkzeug.utils import secure_filename

from api.utils.responses import returnError, returnSuccess
from api.db.collections import get_user_files_collection
from config.logger import setup_logger 

logger = setup_logger(__name__) 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE_MB = 5

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    logger.info("Handling file upload request...")

    if 'file' not in request.files:
        logger.warning("No file part in request")
        return returnError('No file part in request')

    file = request.files['file']
    if file.filename == '' or not file.filename:
        logger.warning("No selected file")
        return returnError('No selected file')

    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type: {file.filename}")
        return returnError('Only CSV files are allowed')

    if file.content_length and file.content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
        logger.warning(f"File too large: {file.content_length} bytes")
        return returnError(f'Max file size is {MAX_FILE_SIZE_MB} MB')

    logger.debug(f"Authenticated user: {g.user}")

    # Secure filename and define save path
    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    try:
        file.save(save_path)
        logger.info(f"File saved to: {save_path}")
    except Exception as e:
        logger.exception("Failed to save file")
        return returnError("Internal server error while saving file")

    try:
        df = pd.read_csv(save_path, nrows=5)
        if df.empty or len(df.columns) < 2:
            logger.warning("Uploaded CSV is empty or has less than 2 columns")
            os.remove(save_path)
            return returnError('CSV must have at least 2 columns and not be empty')
    except Exception as e:
        logger.exception("Error reading uploaded CSV file")
        os.remove(save_path)
        return returnError('Invalid CSV file')

    try:
        get_user_files_collection().insert_one({
            "user_id": g.user['_id'],
            "filename": filename,
            "upload_time": pd.Timestamp.now(),
            "config": None,
            "preprocessed_preview": None,
            "path": save_path
        })
        logger.info(f"File metadata inserted to DB for user_id: {g.user['_id']}")
    except Exception as e:
        logger.exception("Failed to insert file metadata to DB")
        return returnError("Internal server error while saving metadata")

    return returnSuccess('File uploaded and verified', data={'filename': filename})
