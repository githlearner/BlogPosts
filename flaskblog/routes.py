from flask import render_template,url_for,flash,redirect,request
from flaskblog import app,db,bcrypt
from flaskblog.forms import LoginForm,RegistrationForm
from flaskblog.models import User,Post
from flask_login import login_user,logout_user,current_user,login_required

posts = [
    {
        'author':'Githin V George',
        'title':'Python Learning',
        'content': 'I like learning Python',
        'date':'January 30,2019'
    },

    {
        'author': 'Nighisha John',
        'title': 'Master Chef',
        'content': 'I like watching master chef seasons in the TV.',
        'date': 'February 1,2019'
    },

    {
        'author': 'Diya Mary Zachariah',
        'title': 'Drinking milk',
        'content': 'I want to have milk always',
        'date': 'January 23,2019'
    }
]


@app.route('/')
@app.route('/home')
def home():
   return  render_template('home.html',posts=posts)



@app.route('/about')
def about():
    return render_template('about.html',title="About Us")


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}! You are now able to login.'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check the email and password','danger')
    return render_template('login.html',title='Login Page', form=form)

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html',title="Account")
