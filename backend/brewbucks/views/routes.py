from flask import Blueprint, jsonify
from brewbucks.models import db

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/health', methods=['GET'])
def health():
        return jsonify({"status":"Healthy"}),200