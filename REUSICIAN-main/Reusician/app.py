from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from users import get_user, append_user

app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if get_user(user_id):
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if(request.form['username'].strip() == "" or request.form['password'].strip() == ""):
            flash('Please fill in all fields')
            return redirect(url_for('signup'))
  
        if(request.form['password'].strip() != request.form['confirm_password'].strip()):
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        username = request.form['username']
        password = request.form['password']
        if get_user(username):
            flash('Username already exists')
            return redirect(url_for('signup'))

        append_user(username, password)
        # Handle signup logic here (e.g., save user to database)
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user(username) == password:
            login_user(User(username))
            return redirect(url_for('profile'))
        flash('Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/placeholder')
@login_required
def placeholder():
    return render_template('placeholder.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

if __name__ == '__main__':
    app.run(debug=True)