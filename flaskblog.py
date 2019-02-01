from flask import Flask,render_template,url_for,flash,redirect,request
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '851c97bbf386024ca976668627197702'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable= False)
    posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self):
        return "User({},{})".format(self.username,self.email)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(100), nullable= False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return "Post('{self.title},'{self.date_posted}')"

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


if __name__ == "__main__":
    app.run(debug=True)

