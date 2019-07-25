from app.models import User, UserSchema
from flask import jsonify, request

user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True, many=True)


# Create user
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
        user.insert_record()

        return jsonify({"message": "{} added successfully".format(user.username)}), 201
        # return user_schema.dump(record).data, 201
    else:
        return jsonify({"message": "Bad request body. JSON expected."}), 400


# Read one user
def read_one(username):
    user = User.fetch_user_by_username(username=username)

    if not user:
        return jsonify({"message": "User {} not found".format(username)}), 404
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
def update_user(name):
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

        # update record
        if User.check_username(name):
            try:
                User.update_user_by_name(name=name, username=username, email=email)
                return jsonify({"message": "User updated successfully"}), 200
            except Exception as e:
                return jsonify({"message": "Error updating user: {}".format(str(e))}), 500
        else:
            return jsonify({"message": "User {} not found".format(name)})
    else:
        return jsonify({"message": "Bad request body. JSON expected"}), 400


# Delete user
def delete_user(username):
    if User.delete_user_by_username(username):
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "Error deleting user. User not found"}), 500

