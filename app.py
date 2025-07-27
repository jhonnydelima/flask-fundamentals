from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_counter = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    new_task = Task(id=task_id_counter, title=data['title'], description=data.get('description', ''))
    task_id_counter += 1
    tasks.append(new_task)
    return jsonify({'message': 'Nova tarefa criada com sucesso'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'total_tasks': len(tasks)
    })

if __name__ == '__main__':
    app.run(debug=True)