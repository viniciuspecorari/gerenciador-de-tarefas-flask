from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instâncias Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Configurando a tabela de Tasks
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Criando as tabelas do banco de dados
with app.app_context():
    db.create_all()


# Criando rota principal
@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('index.html', tasks=tasks)


# Rota para cadastrar
@app.route('/create/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        data = request.form
        task_content = data.get('content')
        completed = 0
        new_task = Todo(content=task_content, completed=completed)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('create.html')


# Rota para deletar a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task!'


# Rota para atualizar a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form
        task.content = data.get('content')
        varCompleted = data.get('completed')

        if varCompleted == 'on':
            task.completed = 1
        else:
            task.completed = 0

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task!'
    else:
        return render_template('update.html', task=task)


# Rodando o app
if __name__ == "__main__":
    app.run(debug=True)
