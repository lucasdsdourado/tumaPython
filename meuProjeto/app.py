from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore
import os

app = Flask(__name__)

# Configurar Firestore
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credenciais.json'
db = firestore.Client()

@app.route('/')
def index():
    return redirect(url_for('todos'))

@app.route('/todos')
def todos():
    # Buscar todos
    todos_ref = db.collection('todos')
    todos = todos_ref.get()
    
    todo_list = []
    for todo in todos:
        todo_data = todo.to_dict()
        todo_data['id'] = todo.id
        todo_list.append(todo_data)
    
    return render_template('todos.html', todos=todo_list)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    title = request.form['title']
    todo_data = {
        'title': title,
        'completed': False
    }
    
    db.collection('todos').add(todo_data)
    return redirect(url_for('todos'))

@app.route('/toggle_todo/<todo_id>')
def toggle_todo(todo_id):
    todo_ref = db.collection('todos').document(todo_id)
    todo = todo_ref.get()
    
    if todo.exists:
        todo_data = todo.to_dict()
        todo_ref.update({'completed': not todo_data['completed']})
    
    return redirect(url_for('todos'))

@app.route('/edit_todo/<todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo_ref = db.collection('todos').document(todo_id)
    todo = todo_ref.get()
    
    if request.method == 'POST':
        new_title = request.form['title']
        todo_ref.update({'title': new_title})
        return redirect(url_for('todos'))
    
    if todo.exists:
        todo_data = todo.to_dict()
        return render_template('edit_todo.html', todo=todo_data, todo_id=todo_id)
    
    return redirect(url_for('todos'))

@app.route('/delete_todo/<todo_id>')
def delete_todo(todo_id):
    todo_ref = db.collection('todos').document(todo_id)
    todo_ref.delete()
    
    return redirect(url_for('todos'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='5000')