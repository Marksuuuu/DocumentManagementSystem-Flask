from flask import Flask, render_template, jsonify, request, redirect, url_for
import psycopg2
import os
import imghdr
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'marksuuuu'  # Set a secret key for session management

host = 'localhost'
port = '5432'
db_name = 'inventory_system_flask'
db_user = 'flask_user'
db_password = '-clear1125'

conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

cur = conn.cursor()

# Flask-Login setup
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user ID
    cur.execute("SELECT * FROM public.login_details_tbl WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        user_id, username, role = user_data[0], user_data[1], user_data[5]
        return User(user_id, username, role)
    return None


@app.route('/register', methods=['POST'])
def register_insert():
    username = request.form['personUsername']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    uploaded_img = request.files['fileInput']
    role = request.form['role']

    if uploaded_img and allowed_file(uploaded_img.filename):
        filename = secure_filename(uploaded_img.filename)
        file_path = os.path.join('static/assets/img', filename)
        uploaded_img.save(file_path)
        cur.execute(
            "INSERT INTO public.login_details_tbl (username, firstname, lastname, password, user_role, profile, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (username, firstname, lastname, password, role, file_path, email))
        conn.commit()  # commit the transaction
        msg = "INSERT SUCCESS"
    else:
        msg = "Invalid file format. Only image files are allowed."

    return jsonify(msg)


def allowed_file(filename):
    # Define a list of allowed file extensions
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
    # Check if the file extension is in the allowed list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user (perform your own validation logic here)
        cur.execute("SELECT * FROM public.login_details_tbl WHERE username = %s AND password = %s",
                    (username, password))
        user_data = cur.fetchone()

        if user_data:
            user_id, _, role = user_data[0], user_data[1], user_data[5]
            user = User(user_id, username, role)
            login_user(user)  # Log in the user

            # Display user_data and user_role
            print("user_data:", user_data)
            print("user_role:", role)

            if role == 1:
                return redirect(url_for('admin'))  # Redirect to the admin route
            else:
                return redirect(url_for('user'))  # Redirect to the user route
        else:
            return jsonify("Invalid username or password")

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('index'))


@app.route('/admin')
@login_required  # Secure the route, only logged in users can access it
def admin():
    # Admin logic here
    return render_template('admin.html')


@app.route('/user')
@login_required  # Secure the route, only logged in users can access it
def user():
    # User logic here
    return render_template('user.html')


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
