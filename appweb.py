from os import abort, name
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, form
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appweb.db'
db = SQLAlchemy(app)

class Item(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String())
   age = db.Column(db.Integer())
   hometown = db.Column(db.String())
   email = db.Column(db.String())
   datejoin = db.Column(db.String())

   def __init__(self, name, age, hometown, email, datejoin):
      self.name = name
      self.age = age
      self.hometown = hometown
      self.email = email
      self.datejoin = datejoin

@app.route('/')
@app.route('/home')
def home_page():
   return render_template('home.html')

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      Items = Item(request.form['name'], 
      request.form['age'],
      request.form['hometown'], 
      request.form['email'],
      request.form['datejoin'])
      
      db.session.add(Items)
      db.session.commit()

      return redirect(url_for('manage_page'))
   return render_template('new.html')


@app.route('/manage')
def manage_page():
   items = Item.query.all()
   return render_template('manage.html', items= items)

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
   items = Item.query.filter_by(id = id).first()
   if request.method == 'POST':
      items.name = request.form['name']
      items.age = request.form['age']
      items.hometown = request.form['hometown']
      items.email = request.form['email']
      items.datejoin = request.form['datejoin']

      db.session.merge(items)
      db.session.commit()

      return redirect(url_for('manage_page'))
   return render_template('edit.html')

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
   items = Item.query.filter_by(id = id).first()
   if request.method =='POST':
      db.session.delete(items)
      db.session.commit()
      return redirect(url_for('manage_page'))
   return render_template('delete.html')

if __name__ == '__main__':
   db.create_all()
   app.run()
