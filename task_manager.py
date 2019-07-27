from app import app, flask_app, migrate
from flask import jsonify

if __name__ == '__main__':
    # Swagger Documentation
    app.add_api('swagger.yaml')
    app.run(debug=True, host='127.0.0.1', port=5000)
