#  """Models for Flask Feedback App."""

from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_bcrypt import Bcrypt
# from app import app


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for user database and methods"""
    __tablename__ = 'users'

    def __repr__(self):
        e = self
        return f"<User username={e.username}, email={e.email}, full_name={e.full_name}>"
    
    username = db.Column(db.String(20), 
                           nullable=False,
                           unique=True,
                           primary_key=True)
    password = db.Column(db.Text, 
                           nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30), 
                           nullable=False)
    last_name = db.Column(db.String(30), 
                           nullable=False)
    
    @property
    def full_name(self):
        """The full name property"""
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Check to see if user exists, and check that password is correct """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
    
    @classmethod
    def check_errors(cls,err, form):
        """Check error message to determine which constraint contains an error."""
        err_key = err.split(':')[-1].replace('\n', '').strip()
            
        if 'username' in err_key:
            err_msg = 'Username already exists.'
            return form.username.errors.append(err_msg)

        if 'email' in err_key:
            err_msg = 'Email address already exists.  Login instead?'
            return form.email.errors.append(err_msg)
        

class Feedback(db.Model):
    """Model for user feedback and methods"""
    
    __tablename__ = 'feedback'

    id = db.Column(db.Integer,  
                   autoincrement=True,
                   primary_key=True)
    title = db.Column(db.String(100), 
                      nullable=False)
    content = db.Column(db.Text, 
                        nullable = False)
    username = db.Column(db.String(20), 
                         db.ForeignKey('users.username'), 
                         nullable=False)
        

    