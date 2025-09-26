from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user storage
users = {}

# Home route
@app.route("/")
def home():
    return "Welcome to User Management API!"

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# GET single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user})
    return jsonify({"error": "User not found"}), 404

# POST - create new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({user_id: users[user_id]}), 201

# PUT - update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    users[user_id].update(data)
    return jsonify({user_id: users[user_id]})

# DELETE - remove user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({"deleted": deleted})
    return jsonify({"error": "User not found"}), 404



app.run(debug=True)
