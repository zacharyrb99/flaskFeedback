from flask import Flask, render_template, redirect, session, flash
from sqlalchemy.sql import exists
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import FeedbackForm, RegisterForm, LoginForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///feedback_db') #'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret12345')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    if 'user' not in session:
        return redirect('/register')
    else:
        user = User.query.get(session['user'])
        return redirect(f'users/{user.username}')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if 'user' in session:
        user = User.query.get(session['user'])
        return redirect(f'/users/{user.username}')

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        if db.session.query(exists().where(User.username == username)).scalar():
            flash(f'{username} already taken!', 'danger')
            return redirect('/register')
        else:
            new_user = User.register(username, password, email, first_name, last_name)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = new_user.username

            flash('Welcome to my app!', 'success')
            return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if 'user' in session:
        user = User.query.get(session['user'])
        return redirect(f'/users/{user.username}')

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session['user'] = user.username
            flash(f'Welcome back, {user.username}', 'success')
            u = User.query.get_or_404(username)
            return redirect(f'/users/{u.username}')
        else:
            flash('Incorrect username/password!', 'danger')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user')
    flash('Goodbye, see you later!', 'success')
    return redirect('/')

@app.route('/users/<username>')
def secret_page(username):
    if 'user' not in session:
        flash('Please login', 'danger')
        return redirect('/login')
    else:
        user = User.query.get(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template('secret.html', user=user, feedback=feedback)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete user based on username"""
    if 'user' not in session:
        flash('Please login!', 'danger')
        return redirect('/loging')

    user = User.query.get(username)
    if user.username == session['user']:
        session.pop('user')
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username} deleted', 'success')
        return redirect('/')
    else:
        flash("You can't delete another user!", 'danger')
        return redirect('/')

@app.route('/feedback')
def show_feedback():
    if 'user' not in session:
        flash('Login please!', 'danger')
        return redirect('/login')

    all_feedback = Feedback.query.all()
    return render_template('feedback.html', feedback = all_feedback)

@app.route('/feedback/add', methods=['GET', 'POST'])
def add_feedback():
    if 'user' not in session:
        flash('Please login!', 'danger')
        return redirect('/login')

    form = FeedbackForm()
    user = User.query.get(session['user'])

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(new_feedback)
        db.session.commit()

        flash('Feedback submitted!', 'success')
        return redirect(f'/users/{user.username}')
    else:
        return render_template('feedback_form.html', form=form)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Delete feedback based on feedback id"""
    if 'user' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')

    feedback = Feedback.query.get_or_404(id)
    user = User.query.get(session['user'])
    if feedback.username == session['user']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback delete', 'success')
        return redirect(f'/users/{user.username}')
    else:
        flash("You can't delete feedback that wasn't posted by you!", 'danger')
        return redirect('/feedback')

@app.route('/feedback/<int:id>/edit', methods=['GET', 'POST'])
def edit_feedback(id):
    if 'user' not in session:
        flash('Please login!', 'danger')
        return redirect('/login')

    feedback = Feedback.query.get(id)
    form = FeedbackForm(obj=feedback)
    user = User.query.get(session['user'])

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.commit()
        flash('Feedback updated!', 'success')
        return redirect(f'/users/{user.username}')
    else:
        return render_template('edit_feedback.html', form=form, feedback=feedback)

