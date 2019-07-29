from app.models import User, UserSchema, Task, TaskSchema
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required
)
from app import db, app, flask_app
import datetime

user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True, many=True)

task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(strict=True, many=True)


# method to refresh expired access token
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user, fresh=False)
    }
    return jsonify(ret), 200


# Create use
def create_user():
    if request.is_json:
        # fetch the details
        data = request.get_json(force=True)

        username = data['username']
        email = data['email']
        password = data['password']

        # Hash the password
        password_hash = User.set_password_hash(password)

        # Check if username and email exists
        if User.check_username(username):
            return jsonify({"message": "Username already exists"}), 409
        if User.check_email(email):
            return jsonify({"message": "Email already exists"}), 409

        # add user to database
        user = User(username=username, email=email, password=password_hash)
        record = user.insert_record()

        # Create access token
        expiry_days = datetime.timedelta(days=1)
        access_token = create_access_token(identity=record.id, expires_delta=expiry_days, fresh=True)
        refresh_token = create_refresh_token(identity=record.id)

        # add token to database
        record.token = refresh_token
        db.session.commit()

        return jsonify({
            "message": "{} added successfully".format(username),
            "token": access_token
            }), 201

        # return user_schema.dump(record).data, 201
    else:
        return jsonify({"message": "Bad request body. JSON expected."}), 400


# login user
def login_user():
    if request.is_json:
        user_data = request.get_json(force=True)
        username = user_data['username']
        password = user_data['password']

        if User.validate_user(username, password):
            user = User.fetch_user_by_username(username)

            expiry_days = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user.id, expires_delta=expiry_days, fresh=True)
            return jsonify({
                "message": "Login successful",
                "token": access_token
            }), 200
        else:
            return jsonify({
                "message": "Invalid username or password"
            }), 404
    else:
        return jsonify({
            "message": "Invalid request body. JSON expected"
        }), 400


# Read one user
@jwt_required
def read_one(id):
    user = User.fetch_user_by_id(id=id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    else:
        return user_schema.jsonify(user), 200


# Read all users
def read_all():
    users = User.fetch_all_users()

    if len(users) == 0:
        return jsonify({"message": "No users found in database"}), 404
    else:
        result = users_schema.dump(users)
        return jsonify(result.data), 200


# Update user
@jwt_required
@fresh_jwt_required
def update_user(id):
    if request.is_json:
        username = None
        email = None

        # Fetch update details
        user_data = request.get_json(force=True)

        # Check if data contains username and email
        if 'username' in user_data:
            username = user_data['username']
        if 'email' in user_data:
            email = user_data['email']

        user = User.fetch_user_by_id(id)

        # update record
        if user:
            try:
                User.update_user_by_id(id=id, username=username, email=email)
                return jsonify({"message": "User updated successfully"}), 200
            except Exception as e:
                return jsonify({"message": "Error updating user: {}".format(str(e))}), 500
        else:
            return jsonify({"message": "User not found"})
    else:
        return jsonify({"message": "Bad request body. JSON expected"}), 400


# Delete user
@jwt_required
def delete_user(id):
    if User.delete_user_by_id(id):
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "Error deleting user. User not found"}), 500


# Users tasks
@jwt_required
def user_tasks(id):
    user = User.fetch_user_by_id(id)

    if user:
        tasks = tasks_schema.dump(user.tasks).data
        if len(tasks) == 0:
            return jsonify({
                "message": "No tasks found for user"
            }), 404
        else:
            return tasks, 200
    else:
        return jsonify({
            "message": "User not found"
        }), 404


# Fetch one task for user
@jwt_required
def user_single_task(uid, id):
    user = User.fetch_user_by_id(uid)

    if user:
        tasks = tasks_schema.dump(user.tasks).data

        if len(tasks) == 0:
            return jsonify({
                "message": "No tasks found for user"
            }), 404
        else:
            for task in tasks:
                if task['id'] == id:
                    return task, 200
    else:
        return jsonify({
            "message": "User not found"
        }), 404


# Update user task
@jwt_required
def update_user_task(uid, id):
    if request.is_json:
        title = description = status = None

        # Fetch the user
        user = User.fetch_user_by_id(uid)

        if user:
            user_tasks = tasks_schema.dump(user.tasks).data
            task_ids = []

            for task in user_tasks:
                task_ids.append(int(task['id']))

            if int(id) in task_ids:
                # Task body
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
                # return jsonify({"message":"Task updated successfully"}), 200
            else:
                return jsonify({
                    "message": "Task not found."
                }), 404
        else:
            return jsonify({
                "message": "User not found"
            })
    else:
        return jsonify({
            "message": "Invalid task details. JSON expected."
        }), 400


# Delete user task
@jwt_required
def delete_user_task(uid, id):
    # Fetch the user
    user = User.fetch_user_by_id(uid)

    if user:
        user_tasks = tasks_schema.dump(user.tasks).data
        task_ids = []

        for task in user_tasks:
            task_ids.append(int(task['id']))

        if int(id) in task_ids:
            if Task.delete_by_id(id):
                return jsonify({
                    "message": "Task deleted successfully"
                }), 200
            else:
                return jsonify({
                    "message": "Error deleting task. Contact the administrator"
                }), 500
        else:
            return jsonify({
                "message": "Task not found"
            }), 404
    else:
        return jsonify({
            "message": "User not found"
        }), 404

