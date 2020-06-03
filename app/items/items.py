import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.items.utils.file_process_manager import ItemsFileProcessManager


uploader_bp = Blueprint('uploader', __name__)


@uploader_bp.route('/uploader', methods=['POST'])
def uploader():
    if 'file' not in request.files:
        return jsonify({'BadRequest': 'Please send a file'}), 400

    request.files['file'].seek(0)
    file_processor = ItemsFileProcessManager(request.files['file'])
    file_processor.run()

    return jsonify({'message': 'File processed successfully'}), 200


@uploader_bp.route("/")
def list():
    return jsonify({'message': "An item shortly"}), 200
