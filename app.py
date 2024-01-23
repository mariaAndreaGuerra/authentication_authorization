from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length 
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

db = SQLAlchemy(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/')
def redirect_to_register():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login successful!', 'success')
        return redirect(url_for('secret'))

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_profile(username):
    if 'username' in session and session['username'] == username:
        user_info = {'username': username, 'email': 'user@example.com', 'first_name': 'John', 'last_name': 'Doe'}
        return render_template('user_profile.html', user_info=user_info)
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/users/<username>', methods=['GET'])
def user_profile(username):
    if 'username' in session and session['username'] == username:
        user_info = {'username': username, 'email': 'user@example.com', 'first_name': 'John', 'last_name': 'Doe'}
        feedback_list = [{'id': 1, 'title': 'Feedback 1', 'content': 'This is feedback 1'},
                         {'id': 2, 'title': 'Feedback 2', 'content': 'This is feedback 2'}]

        return render_template('user_profile.html', user_info=user_info, feedback_list=feedback_list)
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' in session and session['username'] == username:
        flash('User and associated feedback deleted successfully.', 'success')
        session.clear()
        return redirect(url_for('index'))
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' in session and session['username'] == username:
        if request.method == 'POST':
            flash('Feedback added successfully.', 'success')
            return redirect(url_for('user_profile', username=username))
        return render_template('add_feedback.html')
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback_info = {'id': feedback_id, 'title': 'Feedback Title', 'content': 'Feedback content'}

    if 'username' in session and session['username'] == feedback_info['username']:
        if request.method == 'POST':
            flash('Feedback updated successfully.', 'success')
            return redirect(url_for('user_profile', username=feedback_info['username']))
        return render_template('update_feedback.html', feedback_info=feedback_info)
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback_info = {'id': feedback_id, 'username': 'user1'} 

    if 'username' in session and session['username'] == feedback_info['username']:
        flash('Feedback deleted successfully.', 'success')
        return redirect(url_for('user_profile', username=feedback_info['username']))
    else:
        flash('Unauthorized access. Please log in to access this page.', 'warning')
        return redirect(url_for('login'))


@app.route('/secret')
def secret():
    if 'username' in session:
        return "You made it!"
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None) 
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

