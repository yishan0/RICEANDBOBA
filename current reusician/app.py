from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from users import get_user, append_user
import sqlite3
app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Variable to store comments
comments = []

def get_db():
    conn = sqlite3.connect("posts.db")
    conn.row_factory = sqlite3.Row
    return conn


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

@app.route('/about')
def about():
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

@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        print("Form data: ", request.form)
        email = request.form.get('email')
        name = request.form.get('name')
        item = request.form.get('item')
        value = request.form.get('value')
        lf = request.form.get('lf')
        info = request.form.get('info')


        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO posts (email, name, my_item, looking_for, value, more_info)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, name, item, lf, value, info))

        conn.commit()
        conn.close()
        # Add logic to handle the submitted form data
        flash('Form submitted successfully!')
        return redirect(url_for('support'))
    return render_template('support.html')

@app.route('/forum')
def forum():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch all columns from the posts table
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()
    return render_template('forum.html', posts=rows)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?",(id,))
    post = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        comment = request.form.get('comment', '').strip()
        print(comment)

    return render_template("post.html", post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)