from app.models import Task, TaskSchema
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_current_user, decode_token

task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(strict=True, many=True)


def decode_jwt_token(token):
    # token = request.headers.get('Authorization')
    return decode_token(encoded_token=token)


# add task
@jwt_required
def create_task():
    if request.is_json:
        data = request.get_json(force=True)

        # task details
        title = data['title']
        description = data['description']

        # User's id from token
        uid = get_jwt_identity()
        print(uid)

        task = Task(title=title, description=description, user_id=uid)
        record = task.insert_record()
        # return jsonify({"message": "Task added successfully"}),
        return task_schema.dump(record).data, 201
    else:
        return jsonify({"message": "Bad request body. JSON expected."}), 400


# Fetch one task
@jwt_required
def fetch_one(id):
    task = Task.fetch_one_task(id)
    print(task)

    if not task:
        return jsonify({"message": "Task not found"}), 404
    else:
        return task_schema.dump(task).data, 200


# Fetch all tasks
def fetch_all():
    tasks = Task.fetch_tasks()

    if len(tasks) == 0:
        return jsonify({"message": "No tasks found in database"}), 404
    else:
        return tasks_schema.dump(tasks).data, 200


# Update task
def update_task(id):
    # check whether payload is json
    if request.is_json:
        # Initialize vars to None
        title = description = status = None
        data = request.get_json(force=True)

        # Check if data exists in request
        if u'title' in data:
            title = data['title']
        if u'description' in data:
            description = data['description']
        if u'status' in data:
            status = data['status']

        # instantiate task model and send data to database
        task = Task()
        record = task.update_by_id(id, title=title, description=description, status=status)

        return task_schema.dump(record).data, 200
        # return jsonify({"message":"Task updated successfully"})
    else:
        return jsonify({"message": "Bad request body. JSON expected"}), 400


# Delete task
def delete_task(id):
    task = Task()
    if task.delete_by_id(id):
        return jsonify({"message": "Task deleted successfully"}), 200
    else:
        return jsonify({"message": "Error deleting task. Task not found"}), 404


