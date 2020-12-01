from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask import Blueprint, Response, request, jsonify, abort

from controllers.validator import check_for_required_values
from models.fields import INVENTORY
from controllers.connect import db, Database


inventory = Blueprint('inventory', __name__)

table_name = 'items'
@inventory.route('/api/v1/items', methods=['POST'])
@jwt_required
def add_item():
    """f
    add new item
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, INVENTORY)
    redirect = db.insert_item_into_inventory(data)
    return jsonify({'message':'Item added successfully.'}), 200

@inventory.route('/api/v1/items/<doc_id>', methods=['PUT'])
@jwt_required
def update_item(doc_id):
    """
    Update Items
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, INVENTORY)
    db.update_item(data,doc_id)
    return jsonify({'message':'Successful'}),200


@inventory.route('/api/v1/items', methods=['GET'])
@jwt_required
def get_all_items():
    """
    Get all items
    returns: items
    """
    rows= db.get_all_items()
    return jsonify(rows), 200

@inventory.route('/api/v1/items/<doc_id>', methods=['GET'])
@jwt_required
def get_item(doc_id):
    """
    Get all items
    returns: items
    """
    rows= db.get_item(doc_id)
    return jsonify(rows), 200


@inventory.route('/api/v1/items/<doc_id>', methods=['DELETE'])
@jwt_required
def delete_item(doc_id):
    """
    Delete item
    returns: user data
    """
    db.delete_item(table_name,doc_id)
    return jsonify({'message':'Successfully Deleted'}), 200
