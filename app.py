from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost/todo_db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    new_task = Todo(task=data['task'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added!"})

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": t.id, "task": t.task} for t in todos])

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    todo = Todo.query.get(id)
    if todo:
        todo.task = data['task']
        db.session.commit()
        return jsonify({"message": "Task updated!"})
    return jsonify({"error": "Task not found!"}), 404

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Task deleted!"})
    return jsonify({"error": "Task not found!"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
