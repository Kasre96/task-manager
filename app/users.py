from app.models import User, UserSchema
from flask import jsonify, request

user_schema = UserSchema(strict=True)


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
        record = user.insert_record()

        # return jsonify({"message": "{} added successfully".format(user.username)}), 201
        return user_schema.dump(record).data, 201
    else:
        return jsonify({"message": "Bad request body. JSON expected."}), 400
