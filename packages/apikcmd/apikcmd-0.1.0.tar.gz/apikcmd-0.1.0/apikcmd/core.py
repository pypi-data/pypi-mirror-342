# apikcmd/core.py

import requests

API_URL = "http://127.0.0.1:5000"

def get_all_items():
    response = requests.get(f"{API_URL}/items")
    return response.json()

def get_item(item_id):
    response = requests.get(f"{API_URL}/items/{item_id}")
    return response.json()

def post_item(id_, name, value):
    data = {"id": id_, "name": name, "value": value}
    response = requests.post(f"{API_URL}/items", json=data)
    return response.json()

def update_item(item_id, name=None, value=None):
    data = {}
    if name:
        data["name"] = name
    if value:
        data["value"] = value
    response = requests.put(f"{API_URL}/items/{item_id}", json=data)
    return response.json()

def delete_item(item_id):
    response = requests.delete(f"{API_URL}/items/{item_id}")
    return response.json()

def format_items(items):
    formatted = "{\n"
    for key, value in items.items():
        formatted += f" '{key}': {value},\n"
    return formatted.rstrip(",\n") + "\n}"
