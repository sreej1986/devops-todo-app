# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import uuid

app = Flask(__name__)
CORS(app) # Enable CORS for all origins, adjust in production

todos = {} # In-memory dictionary to store todos

@app.route('/')
def home():
    return "To-Do Backend is Running!"

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(list(todos.values()))

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    if not data or 'task' not in data:
        return jsonify({"error": "Task is required"}), 400
    new_id = str(uuid.uuid4())
    todo = {"id": new_id, "task": data['task'], "completed": False}
    todos[new_id] = todo
    return jsonify(todo), 201 # 201 Created

@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    if id not in todos:
        return jsonify({"error": "To-Do not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    todo = todos[id]
    if 'task' in data:
        todo['task'] = data['task']
    if 'completed' in data:
        todo['completed'] = data['completed']
    return jsonify(todo)

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    if id not in todos:
        return jsonify({"error": "To-Do not found"}), 404
    del todos[id]
    return jsonify({"message": "To-Do deleted"}), 204 # 204 No Content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    