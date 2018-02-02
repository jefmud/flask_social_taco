# basic flask imports
from flask import (abort, Flask, flash, g, redirect, render_template, url_for)

# adding flask_admin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.peewee import ModelView

# adding flask_login 
from flask_login import (LoginManager, UserMixin, login_user, login_required,
                         logout_user, current_user)
# flask WTF
from flask_wtf.csrf import CSRFProtect

# import local database/models
import models
import forms

# For our app run
DEBUG=False # note, I use a third party debugger, you may want to set this to True
PORT=8000
HOST='0.0.0.0'

app = Flask(__name__)
app.secret_key = 'thisIsASecret'
csrf = CSRFProtect(app)
csrf.init_app(app)


# flask-admin setup
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        try:
            if current_user.is_admin:
                return render_template('admin.html')
        except:
            pass # silently fail for unauthorized trying to access admin space
        
        return redirect(url_for('index'))
        
admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminView())
admin.add_view(ModelView(models.User))
admin.add_view(ModelView(models.Taco))

# flask-login setup        
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    """Connect to the database before every request-- making things threadsafe"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user
    
@app.after_request
def after_request(response):
    """Clean up after a request"""
    g.db.close()
    return response
    
@login_manager.user_loader
def load_user(user_id):
    """returns user user based on user_id or None"""
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """show login screen, handle data"""
    if current_user.is_authenticated:
        flash('Please logout first.')
        return redirect(url_for('index'))    
    form = forms.LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = models.User.get(models.User.email==email)
            if user.authenticate(password):
                login_user(user)
                flash('You were successfully logged in', category='success')
                return redirect(url_for('index'))
        except Exception as e:
            print(e)
            
        flash('Incorrect login information', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """logout the user"""
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Please logout before registering a new email', category='warning')
        return redirect(url_for('index'))
    
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(email=form.email.data, password=form.password.data)
        except:
            flash("Problems registering this user = {}".format(form.email.data),
                  category='danger')
        else:
            flash("You have been registered as {}".format(form.email.data))
            return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

@app.route('/taco', methods=['GET','POST'])
@login_required
def taco():
    form = forms.TacoForm()
    
    if form.validate_on_submit():
        try:
            models.Taco.create(
                user=current_user._get_current_object(),
                protein=form.protein.data,
                cheese=form.protein.data,
                extras=form.extras.data,
                shell=form.shell.data
            )
        except Exception as e:
            print(e)
            flash("Problems creating taco record", category="danger")
        return redirect(url_for("index"))
    
    return render_template('taco.html', form=form)
    

@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)

if __name__ == '__main__':
    #models.DATABASE.connect()
    #models.initialize()
    #models.add_default_data()
    app.run(host=HOST, port=PORT, debug=DEBUG)

