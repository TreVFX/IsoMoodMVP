from flask import Flask, request, render_template, redirect, url_for
import random
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teens.db'

db = SQLAlchemy(app)

class teens_register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(100))
    password = db.Column(db.Text)
    confirm_pass = db.Column(db.Text)
    date_made = db.Column(db.DateTime)
    

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/user/<int:user_id>')
def user_page(user_id):
  user = teens_register.query.filter_by(id=user_id).one()
  myid = user_id
  return render_template('user.html', user=user, myid=myid)

@app.route('/add_user', methods=['POST'])
def add_user():
  mail = request.form.get('mail')
  username = request.form.get('username')
  password = request.form.get('password')
  confirm_pass = request.form.get('con_pass')
  if password == confirm_pass:
    user = teens_register(email=mail, username=username, password=password, confirm_pass=confirm_pass, date_made=datetime.now())

    db.session.add(user)
    db.session.commit()

    user = teens_register.query.filter_by(id=user.id).one()
    place ="/user/" + str(user.id)
    return redirect(place)
  return redirect(url_for('signup', message="Passwords don't match"))

@app.route('/login_run', methods=['POST'])
def login_run():
  mail = str(request.form.get("mail"))
  password = request.form.get('password')
  try:
    u = teens_register.query.filter_by(email=mail).first()
    if password == u.password:
      place ="/user/" + str(u.id)
      return redirect(place)
    print("You broke me :( ")
    return redirect('/login')
  except Exception:
    return "<h1>You broke me :(</h1>"

@app.route('/user/<int:user_id>/schedule')
def schedule(user_id):
  user_id = user_id
  return render_template("schedule.html")



if __name__ == "__main__":
  app.debug = True
  app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)