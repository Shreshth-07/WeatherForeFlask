from flask import render_template,url_for,request,redirect,jsonify,flash
import pandas as pd
import numpy as np
import traceback
from datetime import datetime
from pytz import timezone 
from apscheduler.schedulers.background import BackgroundScheduler   
import csv
import pickle
import random



import flaskBlog.function_max as func_max
import flaskBlog.function_min as func_min
import flaskBlog.whatsapp as wa
from flaskBlog.models import User, Todo
from flaskBlog.forms import RegistrationForm, LoginForm
from flask_login import login_user,current_user,logout_user, login_required
from flaskBlog import app, db, bcrypt

# current time
timezone = timezone('America/Argentina/ComodRivadavia')
local_time = datetime.now(timezone).strftime('%d-%m-%Y')

# phrases lists
with open("flaskBlog/frases.txt", "rb") as fp:   # Unpickling
    frases = pickle.load(fp)


def max_temp():
    print('ready to go!!!')
    max_temp = func_max.request_preproc()
    min_temp = func_min.request_preproc()
    with open("flaskBlog/max_temp.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow(max_temp)
    with open("flaskBlog/min_temp.csv","a") as file:
        writer = csv.writer(file)
        writer.writerow(min_temp)
    return render_template("weather.html")



# scheduler
scheduler = BackgroundScheduler(daemon=True, timezone = 'America/Argentina/ComodRivadavia')
scheduler.add_job(func = max_temp,trigger ='cron', hour=13, minute=10)
scheduler.start()


@app.route('/',methods=['GET'])
def index():
    q = request.args.get('q')
    rand = random.randint(0,len(frases))
    return render_template('index.html',today_date=local_time,frases=frases,rand=rand,q=q)       


@app.route('/posts',methods=['GET','POST'])
@login_required
def posts():
    if request.method == 'POST':
        post_content = request.form['content']
        post_quantity = request.form['quantity']
        new_post = Todo(content=post_content,quantity=post_quantity,user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else: # if we dont post, we want to display
        #listita = Todo.query.order_by(Todo.date_created).all() #filter by current_user.id
        listita = Todo.query.filter_by(user_id=current_user.id)
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
@login_required
def weather_forecast():
    with open("flaskBlog/max_temp.csv","r") as file:
        reader = csv.reader(file)
        max_T = list(reader)
        max_T = ''.join([str(elem) for elem in max_T[-1]])
    with open("flaskBlog/min_temp.csv","r") as file:
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


@app.route("/register",methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are ready to login.', 'success')
        return redirect(url_for("login"))
    return render_template('register.html',title='Register',form=form)



@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data): 
            login_user(user,remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")