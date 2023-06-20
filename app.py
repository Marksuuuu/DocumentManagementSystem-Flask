from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
import psycopg2.extras
import os
from werkzeug.utils import secure_filename
import re
import bcrypt

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
    def __init__(self, user_id, username, firstname, lastname, password, role, profile, email, itemInCartCount):
        self.id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.role = role
        self.profile = profile
        self.email = email
        self.itemInCartCount = itemInCartCount



@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the user ID
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.login_details_tbl WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                user_id, username, firstname, lastname, password, role, profile, email = user_data
                cur.execute("SELECT count(*) FROM public.cart_details_tbl WHERE userid = %s", (user_id,))
                cart_data = cur.fetchone()
                itemInCartCount = cart_data[0] if cart_data else 0
                return User(user_id, username, firstname, lastname, password, role, profile, email, itemInCartCount)
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
                'username': data[1],
                'firstname': data[2],
                'lastname': data[3],
                'user_role': data[5],
                'user_pfp': data[6],
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
    try:
        username = request.form['personUsername']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        uploaded_img = request.files['fileInput']
        role = request.form['role']

        # Check if all form fields are provided
        if not (username and firstname and lastname and email and password and uploaded_img and role):
            return jsonify({'error': 'Missing form fields'}), 400

        # Generate a valid salt
        salt = bcrypt.gensalt().decode('utf-8')

        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

        if uploaded_img.filename == '' or not allowed_file(uploaded_img.filename):
            return jsonify({'error': 'Invalid file format. Only image files are allowed.'}), 400

        filename = secure_filename(uploaded_img.filename)
        file_path = os.path.join('static/assets/img', filename).replace("\\", "/")
        uploaded_img.save(file_path)

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.login_details_tbl (username, firstname, lastname, password, user_role, profile, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (username, firstname, lastname, hashed_password, role, file_path, email))
                conn.commit()
                msg = "INSERT SUCCESS"
                return jsonify({'message': msg}), 200

    except KeyError:
        return jsonify({'error': 'Invalid form data'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/updateUserData', methods=['POST'])
def update_user_data():
    input_username = request.form['inputUsername']
    input_first_name = request.form['inputFirstName']
    input_last_name = request.form['inputLastName']
    input_email_address = request.form['inputEmailAddress']
    password = request.form['passwordID']  # New password entered by the user
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
                    if password:
                        # Generate a valid salt
                        salt = bcrypt.gensalt().decode('utf-8')

                        # Hash the new password with the salt
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

                        cur.execute(f"UPDATE public.login_details_tbl SET username='{input_username}', firstname='{input_first_name}', lastname='{input_last_name}', password='{hashed_password}', profile='{file_path}', email='{input_email_address}' WHERE id = {user_id};")
                    else:
                        cur.execute(f"UPDATE public.login_details_tbl SET username='{input_username}', firstname='{input_first_name}', lastname='{input_last_name}', profile='{file_path}', email='{input_email_address}' WHERE id = {user_id};")

                    conn.commit()  # commit the transaction
                    msg = 'UPDATE SUCCESS'
        else:
            msg = 'Invalid file format. Only image files are allowed.'
    else:
        msg = False

    return jsonify(msg)


@app.route('/process-csv', methods=['POST'])
def process_csv():
    file = request.files['file']
    lines = file.read().decode('utf-8').split('\n')

    # Process the CSV data and insert into the database table
    for line in lines:
        columns = line.split(',')
        if len(columns) != 6:
            # Handle the case where the number of columns is incorrect
            continue  # Skip this row and move to the next

        productName = columns[0]
        productCount = columns[1]
        file_path = columns[2]  
        productPrice = columns[3]
        productDescription = columns[4]
        productTypes = columns[5]

        # Validate productPrice as an integer
        if not productPrice.isdigit():
            # Handle the case where productPrice is not a valid integer
            productPrice = 0  # Assign a default value or handle it as appropriate

        # Execute the SQL query to insert data into the table
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.product_details_tbl (productname, productcount, fileuploaded, productprice, productdescription, producttypes) VALUES (%s, %s, %s, %s, %s, %s)",
                    (productName, productCount, file_path, int(productPrice), productDescription, productTypes))
                conn.commit()  # commit the transaction
                msg = "INSERT SUCCESS"

    return jsonify(msg)



@app.route('/upload', methods=['POST'])
def upload_insert():
    productName = request.form['productName']
    productCount = request.form['productCount']
    fileUploaded = request.files['fileUploaded']
    productPrice = request.form['productPrice']
    productDescription = request.form['productDescription']
    productTypes = request.form['productTypes']

    # Check if the product already exists in the database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM public.product_details_tbl WHERE productname = %s", (productName,))
            count = cur.fetchone()[0]
            if count > 0:
                msg = "Product already exists in the database."
                return jsonify(msg)

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


@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    user_id = request.form['userId']
    item_id = request.form['data_id']
    prodCount = request.form['prodCount']
    itemImg = request.form['itemImg']
    productPrice = request.form['productPrice']
    productName = request.form['productName']

    itemImgPath = '../static/assets/img/products/'+itemImg
    # Remove "Price: 0" using regex
    productPrice = re.sub(r'Price: ', '', productPrice)

    print(productPrice)

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO public.cart_details_tbl (itemid, userid, productname, productcount, fileuploaded, productprice) VALUES (%s, %s, %s, %s, %s, %s)",
                (int(item_id), int(user_id), productName, int(prodCount), itemImgPath, int(productPrice)))
            conn.commit()  # commit the transaction
            msg = "INSERT SUCCESS"

    return jsonify(msg)






@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.login_details_tbl WHERE username = %s", (username,))
                user_data = cur.fetchone()

        if user_data:
            stored_password = user_data[4]  # Get the hashed password from the database
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                user_id, username, firstname, lastname, password, role, profile, email = user_data
                itemInCartCount = 0  # Assign a value to itemInCartCount
                user = User(user_id, username, firstname, lastname, password, role, profile, email, itemInCartCount)
                login_user(user)

                if role == 1:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('user'))
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
    itemInCartCount = current_user.itemInCartCount
    print(itemInCartCount)
    user_id = current_user.id
    profile = current_user.profile
    role = current_user.role
    add_dot = '../'+profile 
    print(user_id)
    return render_template('inventory.html', profile=add_dot, role=role, user_id=user_id, itemInCartCount=itemInCartCount)

@app.route('/uploadProducts')
@login_required
def uploadProducts():
    itemInCartCount = current_user.itemInCartCount
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    return render_template('uploadProducts.html', profile=add_dot, role=role)


@app.route('/myAccount')
@login_required
def myAccount():
    itemInCartCount = current_user.itemInCartCount
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
    itemInCartCount = current_user.itemInCartCount
    user_id = current_user.id
    profile = current_user.profile
    add_dot = '../'+profile 
    role = current_user.role
    firstname = current_user.firstname
    lastname = current_user.lastname
    email = current_user.email
    password = current_user.password
    return render_template('user.html', profile=add_dot, role=role, firstname=firstname, password=password, user_id=user_id)


@app.route('/admin')
@login_required  # Secure the route, only logged in users can access it
def admin():
    itemInCartCount = current_user.itemInCartCount
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
    itemInCartCount = current_user.itemInCartCount
    user_id = current_user.id
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
