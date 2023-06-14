from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
import psycopg2.extras
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.secret_key = 'marksuuuu'  # Set a secret key for session management

# Database configuration
db_config = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'inventory_system_flask',
    'user': 'flask_user',
    'password': '-clear1125'
}

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, role, profile):
        self.id = user_id
        self.username = username
        self.role = role
        self.profile = profile


@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user ID
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.login_details_tbl WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                user_id, username, role, profile = user_data[0], user_data[1], user_data[5], user_data[6]
                return User(user_id, username, role, profile)
    return None


def allowed_file(filename):
    # Define a list of allowed file extensions
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
    # Check if the file extension is in the allowed list
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/getUsers')
def getUsers():
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM public.login_details_tbl")
        user_datas = cursor.fetchall()
        userData = []
        for data in user_datas:
            userData.append({
                'id': data[0],
                'fistname': data[1],
                'lastname': data[2],
                'user_role': data[5],
                'email': data[7]
            })
        cursor.close()
    return jsonify({'data': userData})


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
        file_path = os.path.join('static/assets/img', filename).replace("\\", "/")
        uploaded_img.save(file_path)

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.login_details_tbl (username, firstname, lastname, password, user_role, profile, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (username, firstname, lastname, password, role, file_path, email))
                conn.commit()  # commit the transaction
                msg = "INSERT SUCCESS"
    else:
        msg = "Invalid file format. Only image files are allowed."

    return jsonify(msg)



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user (perform your own validation logic here)
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.login_details_tbl WHERE username = %s AND password = %s",
                            (username, password))
                user_data = cur.fetchone()

        if user_data:
            user_id, _, role, profile = user_data[0], user_data[1], user_data[5], user_data[6]
            user = User(user_id, username, role, profile)
            login_user(user)  # Log in the user

            if role == 1:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user'))  # Redirect to the user route
        else:
            return jsonify("Invalid username or password")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('login'))


@app.route('/uploadProducts')
@login_required
def uploadProducts():
    profile = current_user.profile
    add_dot = '../'+profile 
    return render_template('uploadProducts.html', profile=add_dot)


@app.route('/view_users')
@login_required 
def view_users():
    profile = current_user.profile
    add_dot = '../'+profile 
    return render_template('user.html', profile=add_dot)


@app.route('/admin')
@login_required  # Secure the route, only logged in users can access it
def admin():
    # Admin logic here
    profile = current_user.profile
    add_dot = '../'+profile 
    print(add_dot)
    return render_template('admin.html', profile=add_dot)


@app.route('/user')
@login_required  # Secure the route, only logged in users can access it
def user():
    profile = current_user.profile  # Get the profile image path from the current user
    add_dot = '../'+profile 
    print(add_dot)
    return render_template('user.html', profile=add_dot)


@app.route('/register', methods=['GET'])
def register():
    # User logic here
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='10.0.2.150', port=3000, debug=True)
