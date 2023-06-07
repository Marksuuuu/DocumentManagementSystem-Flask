from flask import Flask, render_template, jsonify, request
import psycopg2
import os
import imghdr
from werkzeug.utils import secure_filename

app = Flask(__name__)

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


@app.route('/register', methods=['POST'])
def registerInsert():
    username = request.form['personUsername']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    uploadedImg = request.files['fileInput']
    role = request.form['role']

    if uploadedImg and allowed_file(uploadedImg.filename):
        filename = secure_filename(uploadedImg.filename)
        file_path = os.path.join('static/assets/img', filename)
        uploadedImg.save(file_path)
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
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
