from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user
from flask import Flask
import hashlib
from uuid import uuid4
from exceptions import SignUpException, LoginException


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/users.db'
application.config['SECRET_KEY'] = 'kkny_secrets'

sql_alchemy = SQLAlchemy(application)

login_manager = LoginManager()
login_manager.init_app(application)


class User (UserMixin, sql_alchemy.Model):
    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    email = sql_alchemy.Column(sql_alchemy.String(30), unique=True)
    password = sql_alchemy.Column(sql_alchemy.String(35))
    first_name = sql_alchemy.Column(sql_alchemy.String(30))
    last_name = sql_alchemy.Column(sql_alchemy.String(30))
    gender = sql_alchemy.Column(sql_alchemy.String(6))


class Signup:
    def __init__(self, sign_up_form):
        self.sign_up_form = sign_up_form

    def validate_signup(self) -> dict:
        if '' in [sign_up_form_value.strip() for sign_up_form_value in self.sign_up_form.values()]:
            raise SignUpException('There are missing fields')

        if self.sign_up_form['password'] != self.sign_up_form_info['repeat_password']:
            raise SignUpException('Passwords are not matching ')

        if len(self.sign_up_form['password']) > 35:
            raise SignUpException('Password must not be above 35 characters')

        if '@' not in self.sign_up_form['email'] or '.com' not in \
                self.sign_up_form['email']:
            raise SignUpException('Please enter only valid emails')

    def signup_user(self):
        salt = uuid4().hex
        encrypted_password = hashlib.sha256(
            salt.encode() +
            self.sign_up_form['password'].encode()
        ).hexdigest() + ':' + salt

        new_user = User(email=self.sign_up_form['email'],
                        password=encrypted_password,
                        first_name=self.sign_up_form['first_name'],
                        last_name=self.sign_up_form['last_name'],
                        gender=self.sign_up_form['gender'])

        sql_alchemy.session.add(new_user)
        sql_alchemy.session.commit()
        login_user(new_user)


class Login:
    def __init__(self, login_form):
        self.login_form = login_form
        self.logged_in_user = None

    def validate_login(self) -> dict:
        self.logged_in_user = User.query.filter_by(email=self.login_form['email']).first()

        if not self.logged_in_user:
            raise LoginException('A user with this email / password combination does not exist')

    def login_user(self):
        encrypted_password, salt = self.logged_in_user.split(':')

        if encrypted_password == hashlib.sha256(salt.encode() +
                                                self.login_form['password'].encode()).hexdigest():
            login_user(self.logged_in_user)

        raise LoginException('A user with this email / password combination does not exist')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

