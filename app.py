from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory storage
tasks = []
next_id = 1


# ✅ GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


# ✅ POST create new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id

    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()

    title = data.get('title', '')
    description = data.get('description', '')

    if not title.strip():
        return jsonify({"error": "Title cannot be empty"}), 400

    task = {
        "id": next_id,
        "title": title.strip(),
        "description": description.strip(),
        "done": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# ✅ GET single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        abort(404, description="Task not found")

    return jsonify(task)


# ✅ UPDATE task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        abort(404, description="Task not found")

    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()

    title = data.get('title', task['title'])

    if not title.strip():
        return jsonify({"error": "Title cannot be empty"}), 400

    task['title'] = title.strip()
    task['description'] = data.get('description', task['description']).strip()
    task['done'] = data.get('done', task['done'])

    return jsonify(task)


# ✅ DELETE task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    task = next((t for t in tasks if t['id'] == task_id), None)

    if task is None:
        abort(404, description="Task not found")

    tasks = [t for t in tasks if t['id'] != task_id]

    return jsonify({"message": "Task deleted"}), 200


# ✅ Optional home route
@app.route('/')
def home():
    return "Task Manager API is running 🚀"


# ✅ Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)