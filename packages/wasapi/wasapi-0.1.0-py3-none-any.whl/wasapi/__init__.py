# app_module.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory dictionary
items = {}

@app.route("/", methods=["GET"])
def home():
    return "API is running!"

@app.route("/items", methods=["GET"])
def get_all_items():
    return jsonify(items)

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if item_id in items:
        return jsonify({item_id: items[item_id]})
    return ("Item not found", 404)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    item_id = data.get("id")
    name = data.get("name")
    value = data.get("value")

    if None in (item_id, name, value):
        return ("Missing 'id', 'name' or 'value'", 400)

    if item_id in items:
        return ("Item with this ID already exists", 400)

    items[item_id] = {"name": name, "value": value}
    return jsonify({item_id: items[item_id]}), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id not in items:
        return ("Item not found", 404)

    data = request.get_json()
    name = data.get("name")
    value = data.get("value")

    if name:
        items[item_id]["name"] = name
    if value:
        items[item_id]["value"] = value

    return jsonify({item_id: items[item_id]})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in items:
        del items[item_id]
        return jsonify({"message": "Deleted"}), 200
    return ("Item not found", 404)

