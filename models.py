# python imports
import datetime

# flask bcrypt for passwords
from flask_bcrypt import generate_password_hash, check_password_hash

# basic peewee import style
from peewee import *

# magic from flask_login
from flask_login import UserMixin

DATABASE = SqliteDatabase('taco.db')

class User(UserMixin, Model):
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    
    @classmethod
    def create_user(cls, email, password, is_admin=False):
        hashed_password = generate_password_hash(password)
        try:
            with DATABASE.transaction():
                cls.create(email=email, password=hashed_password, is_admin=is_admin)
        except IntegrityError:
            raise ValueError('username or email already exists')
    
    def authenticate(self, password):
        if check_password_hash(self.password, password):
            return True
        return False
    
    def reset_password(self, password):
        self.password = generate_password_hash(password)
        self.save()
        
    def __repr__(self):
        return self.email
        
    class Meta:
        database = DATABASE
        order_by = ('email',)
        
class Taco(Model):
    user = ForeignKeyField(User, related_name='user')
    protein = CharField(default='chicken')
    shell = CharField(default='flour')
    cheese = BooleanField(default=True)
    extras = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE
        order_by = ('protein',)
        
def fix_unencrypted_passwords():
    """if an admin changes a password with flask-admin, this must be called for maintenance"""
    # this may be unecessary if I override the create method, but could have database
    # portability implications
    users = User.select()
    for user in users:
        try:
            # authentication should throw an error on a non-hashed password
            user.authenticate(user.password)
        except:
            # encrypt/hash current password
            user.reset_password(user.password)
        
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Taco],safe=True)
    
def add_default_data(debug=False):
    """add default data, should only be run after initialize since DATABASE should be connected"""
    try: User.create_user(email='admin@local.net', password='secret', is_admin=True)
    except Exception as e:
        if debug: print(str(e))
    try: User.create_user(email='joe@local.net', password='joesecret', is_admin=False)
    except Exception as e:
        if debug: print(str(e))
        
        
    #user = User.select().get()
    Taco.create(
            user=user,
            protein='chicken',
            shell='flour',
            cheese=False,
            extras='Gimme some guac.'
        )
    #taco = Taco.select().get()    