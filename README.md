# flask_social_taco
flask social network exercise for taco appreciation

This app was done as an exercise to demonstrate a simple social media site with user logins, registration,
ORM backend, and administration interface.  It represents a good starting point for a more fully developed
project.

I don't expect anyone to even want to look at this except me to reference the internal techniques.

## It has:

* User Login, logout, registration
* Peewee ORM of two models: User, Taco, password hashing, encryption
* Flask-admin interface (in homage to Django's out of the box administration)
* simple custom templates/styling (not designed by me)
* unit tests in separate module (slightly modified from Kenneth Love's design)

The app may seem a little strange.  It allows users to register, and enter Taco combinations they have tried or want
to create. Kind of weird, but you can see the possibilities of enhanced data like recipe, review, journaling.

## What it lacks:
No RSS feed; No email notification; No social "Follow/Unfollow"; No API

Perhaps these can be added as additional exercise?

## The environment:

### Built under Python 3.6, should work on Mac, Windows, or Linux

comments- modern pip will install everything through the process. Flask bootstrap is optional and was
unused because I was provided with the CSS by Kenneth Love

```
# this will vary with your setup for virtual environments,
# what I present reflects a common Linux scenario
$ sudo apt install virtualenv
$ ~/Python36/scripts/virtualenv ~/env/fenv3 
$ source ~/env/fenv3/bin/activate
(fenv3) $ pip install flask
(fenv3) $ pip install peewee
(fenv3) $ pip install flask-admin
(fenv3) $ pip install flask-login
(fenv3) $ pip install flask-bcrypt
(fenv3) $ pip install flask-bootstrap
(fenv3) $ pip install flask-wtf
(fenv3) $ pip install wtf-peewee
(fenv3) $ pip freeze

bcrypt==3.1.4
cffi==1.11.4
click==6.7
dominate==2.3.1
Flask==0.12.2
Flask-Admin==1.5.0
Flask-Bcrypt==0.7.1
Flask-Bootstrap==3.3.7.1
Flask-Login==0.4.1
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
peewee==2.10.2
pycparser==2.18
six==1.11.0
visitor==0.1.3
Werkzeug==0.14.1
wtf-peewee==0.2.6
WTForms==2.1
```
