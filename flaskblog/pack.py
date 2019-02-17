from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog.models import User
from flaskblog import app,mail
from flask_mail import Message
from celery import Celery


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
celery = Celery(app.name,broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def validate_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)
        print(user_id)
    except:
        return None
    return User.query.get(user_id['user_id'])

@celery.task
def send_reset_email(user):
    msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''Celery Mail Test
    '''
    mail.send(msg)


u = User.query.get(6)
task = send_reset_email.apply_async(args=[u],countdown=60)