from flask import render_template,url_for,flash,redirect
from flaskblog import app
from flaskblog.forms import LoginForm,RegistrationForm
from flaskblog.models import User,Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',title='Login Page', form=form)