import os

from flask import Blueprint, request, jsonify
from app.models.service import Service
from app.extensions import db

route = os.getenv('FLASK_ROUTE', '/')
services_bp = Blueprint('services', __name__, url_prefix=route + 'services')


@services_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    