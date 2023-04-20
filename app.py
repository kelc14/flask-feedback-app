# """Flask Feedback application."""

from flask import Flask, request, redirect, render_template, flash, url_for, session
from models import db, connect_db, User, Feedback
from sqlalchemy.exc import IntegrityError

from forms import RegistrationForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

# from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'secret123!'
# debug = DebugToolbarExtension(app)

@app.route('/')
def show_home():
    """redirect to the registration page"""
    return redirect('/register')

@app.route('/users/<username>')
def show_user(username):
    """Secret page, only shown to authenticated users."""
    if 'username' not in session:
        flash('You must be logged in to view!')
        return redirect(url_for('show_login'))
    if session['username'] != username:
        flash('Unauthorized!')
        return redirect(url_for('show_user', username=session['username']))
    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter_by(username=username).all()

    return render_template('secret.html', user=user, feedbacks=feedback)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if 'username' not in session:
        flash('Please login first.')
        return redirect('/login')
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('User deleted.')
        return redirect('/')        
    else:
        flash('Not authorized.')
        user = session['username']
        return redirect(f'/users/{user}')

# Feedback Routes 
  
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def show_feedback_form(username):
    if 'username' not in session:
        flash('Please login first.')
        return redirect('/login')
    
    if session['username'] != username:
        flash('Unauthorized User.')
        return redirect(url_for('show_user', username=username))
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('New feedback added!')
        return redirect(url_for('show_user', username=username))
            
    return render_template('feedback.html', form=form)
    

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session:
        flash('Please login first.')
        return redirect('/login')
    
    if session['username'] != feedback.username:
        flash('Unauthorized User.')
        return redirect(url_for('show_user', username=feedback.username))
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()
        flash('Updated feedback!')
        return redirect(url_for('show_user', username=feedback.username))

    
    return render_template('edit_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session:
        flash('Please login first.')
        return redirect('/login')
    if session['username'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted.')
        return redirect(f'/users/{feedback.username}')        
    else:
        flash('Not authorized.')
        user = session['username']
        return redirect(url_for('show_user', username=user)) 



#  ********************************************
#               LOGIN AND REGISTRATION
#  ********************************************

@app.route('/register', methods=["GET", "POST"])
def show_registration():

    if 'username' in session:
        return redirect(url_for('show_user', username=session['username']))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        first_name=first_name.capitalize()
        last_name=form.last_name.data
        last_name=last_name.capitalize()


        new_user=User.register(username, password, email, first_name, last_name)
        
        db.session.add(new_user)

        try: 
            db.session.commit()
        except IntegrityError as e:
            err = str(e.orig)
            User.check_errors(err, form)
            return render_template('registration.html', form=form)

        flash(f"Registration Complete! Welcome {new_user.full_name}")

        session['username'] = new_user.username

        return redirect(f'/users/{username}')
    
    return render_template('registration.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def show_login():
    if 'username' in session:
        return redirect(url_for('show_user', username=session['username']))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username,pwd)

        if user:
            session['username'] = user.username
            
            return redirect(f'/users/{username}')
        
        else:
            form.username.errors = ['Incorrect username/password. Try again.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'username' not in session:
        flash('Please login first.')
        return redirect('/login')
    
    else:
        session.pop('username')
        flash('Successfully logged out.')
        return redirect('/register')
