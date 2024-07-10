from flask import Flask,render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy 
import os 


# Connection with database  
file_path = os.path.abspath(os.getcwd())+"/todo.db"
  
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path 
db = SQLAlchemy(app) 



#Table creation in database
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(200))
    complete = db.Column(db.Boolean)


    def __repr__(self):
        return self.text
    

 
with app.app_context():
    db.create_all()

#Routes Allocation for each function

@app.route('/')

def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete= Todo.query.filter_by(complete=True).all()


    return render_template('index.html', incomplete=incomplete,
                           complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo=Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
def complete(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complete=True

    db.session.commit()

    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)
     
    

