from flask import Flask,render_template,url_for,request,redirect,jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import numpy as np
import traceback
from datetime import datetime
from pytz import timezone 
from apscheduler.schedulers.background import BackgroundScheduler   
import csv
import function_max as func_max
import function_min as func_min
import whatsapp as wa
import pickle
import random



#from sklearn.externals import joblib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

# current time
timezone = timezone('America/Argentina/ComodRivadavia')
local_time = datetime.now(timezone).strftime('%d-%m-%Y')

# phrases lists
with open("frases.txt", "rb") as fp:   # Unpickling
    frases = pickle.load(fp)


def max_temp():
    print('ready to go!!!')
    max_temp = func_max.request_preproc()
    min_temp = func_min.request_preproc()
    with open("max_temp.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow(max_temp)
    with open("min_temp.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow(min_temp)
    return render_template("weather.html")



# scheduler
scheduler = BackgroundScheduler(daemon=True, timezone = 'America/Argentina/ComodRivadavia')
scheduler.add_job(func = max_temp,trigger ='cron', hour=13, minute=10)
scheduler.start()




class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True) # these will be unique
    content = db.Column(db.Text, nullable=False) # the user cannot leave it empty
    quantity = db.Column(db.String(10),nullable=False,default='no importa')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #this function occurs every time we create a new element
    def __repr__(self):
        return 'Task' + str(self.id)



@app.route('/',methods=['POST','GET'])
def index():
    rand = random.randint(0,len(frases))
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html',today_date=local_time,frases=frases,rand=rand)       

@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_content = request.form['content']
        post_quantity = request.form['quantity']
        new_post = Todo(content=post_content,quantity=post_quantity)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else: # if we dont post, we want to display
        listita = Todo.query.order_by(Todo.date_created).all()
        return render_template('posts.html', reyes=listita)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Todo.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/delete/all')
def delete_all():
    db.session.query(Todo).delete()
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = Todo.query.get_or_404(id)
    if request.method == 'POST': # if you are in the new /edit/id and you press POST, then do this
        post.content = request.form['content']
        post.quantity = request.form['quantity']
        db.session.commit()
        return redirect('/posts')
    else:  # before pressing we should see...
        return render_template('edit.html',post=post)
    
@app.route('/weather')
def weather_forecast():
    with open("max_temp.csv","r") as file:
        reader = csv.reader(file)
        max_T = list(reader)
        max_T = ''.join([str(elem) for elem in max_T[-1]])
    with open("min_temp.csv","r") as file:
        reader = csv.reader(file)
        min_T = list(reader)
        min_T = ''.join([str(elem) for elem in min_T[-1]])
    return render_template('weather.html',max_T=max_T,min_T=min_T)

@app.route('/posts/send/all')
def send_all():
    whole_list = []
    for item in db.session.query(Todo).all():
        whole_list.append((item.quantity,item.content))
    b = ''
    for i,j in whole_list:
        b = b + '\u2022' + (i + ' ' + j + '    ' )
    print(b)

    #wa.send_WA(b)
    return redirect('/posts')

@app.route('/numero')
def numero():
    render_template('index.html')

@app.route('/about',methods=['GET'])
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))




