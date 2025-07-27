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
  return jsonify({'message': 'Nova tarefa criada com sucesso'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
  return jsonify({
    'tasks': [task.to_dict() for task in tasks],
    'total_tasks': len(tasks)
  })

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for task in tasks:
    if task.id == id:
      return jsonify(task.to_dict())
  return jsonify({'message': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  data = request.get_json()
  for task in tasks:
    if task.id == id:
      task.title = data.get('title', task.title)
      task.description = data.get('description', task.description)
      return jsonify({'message': 'Tarefa atualizada com sucesso'})
  return jsonify({'message': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:id>', methods=['PATCH'])
def toggle_task_completion(id):
  for task in tasks:
    if task.id == id:
      task.completed = not task.completed # toggle the completion status
      return jsonify({'message': 'Status da tarefa atualizado com sucesso'})
  return jsonify({'message': 'Tarefa não encontrada'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  task = None
  for t in tasks:
    if t.id == id:
      task = t
      break
  if not task:
    return jsonify({'message': 'Tarefa não encontrada'}), 404
  tasks.remove(task)
  return jsonify({'message': 'Tarefa removida com sucesso'})

if __name__ == '__main__':
  app.run(debug=True)