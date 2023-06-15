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
    def __init__(self, user_id, username, firstname, lastname, password, role, profile, email):
        self.id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.role = role
        self.profile = profile
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user ID
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.login_details_tbl WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                user_id, username, firstname, lastname, password, role, profile, email = user_data[0],user_data[1],user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7]
                return User(user_id, username, firstname, lastname, password, role, profile, email)
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


@app.route('/inventory')
def get_inventory():
    with psycopg2.connect(**db_config) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM public.product_details_tbl")
        rows = cursor.fetchall()
        category_data = []
        for row in rows:
            category_data.append({
                'id': row[0],
                'productName': row[1],
                'productCount': row[2],
                'fileUploaded': row[3],
                'productPrice': row[4],
                'productDescription': row[5],
                'productTypes': row[6],
            })
        cursor.close()
    return jsonify({'data': category_data})


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


@app.route('/updateUserData', methods=['POST'])
def update_user_data():
    input_username = request.form['inputUsername']
    input_first_name = request.form['inputFirstName']
    input_last_name = request.form['inputLastName']
    input_email_address = request.form['inputEmailAddress']
    role = request.form['role']
    password_id = request.form['passwordID']
    user_id = request.form['userId']

    if 'profileImg' in request.files:
        profile_img = request.files['profileImg']
        if profile_img.filename == '':
            msg = 'No file selected.'
        elif profile_img and allowed_file(profile_img.filename):
            filename = secure_filename(profile_img.filename)
            file_path = os.path.join('static/assets/img', filename).replace("\\", "/")
            profile_img.save(file_path)

            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"UPDATE public.login_details_tbl SET username='{input_username}', firstname='{input_first_name}', lastname='{input_last_name}', password='{password_id}', profile='{file_path}', email='{input_email_address}' WHERE id = {user_id};")
                    conn.commit()  # commit the transaction
                    msg = 'INSERT SUCCESS'
        else:
            msg = 'Invalid file format. Only image files are allowed.'
    else:
        msg = 'Profile image not found in the request.'

    return jsonify(msg)

@app.route('/upload', methods=['POST'])
def upload_insert():
    productName = request.form['productName']
    productCount = request.form['productCount']
    fileUploaded = request.files['fileUploaded']
    productPrice = request.form['productPrice']
    productDescription = request.form['productDescription']
    productTypes = request.form['productTypes']

    if fileUploaded and allowed_file(fileUploaded.filename):
        filename = secure_filename(fileUploaded.filename)
        file_path = os.path.join('static/assets/img/products', filename).replace("\\", "/")
        fileUploaded.save(file_path)

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.product_details_tbl (productname, productcount, fileuploaded, productprice, productdescription, producttypes) VALUES (%s, %s, %s, %s, %s, %s)",
                    (productName, productCount, file_path, productPrice, productDescription, productTypes))
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
            user_id, username, firstname, lastname, password, role, profile, email = user_data[0],user_data[1],user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7]
            user = User(user_id, username, firstname, lastname, password, role, profile, email)
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


@app.route('/viewInventory')
@login_required
def viewInventory():
    profile = current_user.profile
    role = current_user.role
    add_dot = '../'+profile 
    return render_template('inventory.html', profile=add_dot, role=role)

@app.route('/uploadProducts')
@login_required
def uploadProducts():
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    return render_template('uploadProducts.html', profile=add_dot, role=role)


@app.route('/myAccount')
@login_required
def myAccount():
    user_id = current_user.id
    print('id', user_id)
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    password = current_user.password
    return render_template('account.html', profile=add_dot, role=role, firstname=firstname, password=password, user_id=user_id)


@app.route('/view_users')
@login_required 
def view_users():
    user_id = current_user.id
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    print(role)
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    password = current_user.password
    return render_template('user.html', profile=add_dot, role=role, firstname=firstname, password=password, user_id=user_id)


@app.route('/admin')
@login_required  # Secure the route, only logged in users can access it
def admin():
    # Admin logic here
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    password = current_user.password
    return render_template('admin.html', profile=add_dot)


@app.route('/user')
@login_required  # Secure the route, only logged in users can access it
def user():
    user_id = current_user.id
    print('id', user_id)
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    password = current_user.password
    return render_template('user.html', profile=add_dot, role=role, firstname=firstname, password=password, user_id=user_id)


@app.route('/register', methods=['GET'])
def register():
    # User logic here
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='10.0.2.150', port=3000, debug=True)
