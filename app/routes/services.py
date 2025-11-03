import os

from flask import Blueprint, request, jsonify
from app.models.services import Service
from app.extensions import db

route = os.getenv('FLASK_ROUTE', '/')
services_bp = Blueprint('services', __name__, url_prefix=route + 'services')


@services_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    service = Service(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        image_url=data.get('image_url'),
        is_active=bool(data.get('is_active'))
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Service created'}), 201


@services_bp.route('/', methods=['GET'])
def get_all():
    services = Service.query.all()
    services_list = [{
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'image_url': service.image_url,
        'is_active': service.is_active
    } for service in services]

    return jsonify(services_list), 200


@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    
    return jsonify({
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'image_url': service.image_url,
        'is_active': service.is_active
    }), 200


@services_bp.route('/<int:service_id>', methods=['DELETE'])
def delete(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}), 200


@services_bp.route('/<int:service_id>', methods=['PATCH'])
def update(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    
    data =  request.get_json()
    service.name = data.get('name', service.name)
    service.description = data.get('description', service.description)
    service.price = data.get('price', service.price)
    service.image_url = data.get('image_url', service.image_url)
    service.is_active = bool(data.get('is_active', service.is_active))
    db.session.commit()
    return jsonify({'message': 'Service updated'}), 200
