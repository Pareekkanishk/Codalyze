import os
import psycopg2
from flask import Flask, render_template, request, send_file, session, redirect, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from code_review import analyze_code, fix_code
from pdf_export import generate_pdf

from flask_sqlalchemy import SQLAlchemy
from models import db, User


app = Flask(__name__)                              #Initialize app
app.config['UPLOAD_FOLDER'] = 'uploads'


load_dotenv()                                      #Load environment variables
app.secret_key = os.getenv('SECRET_KEY')


app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}" #For connecting to the Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bcrypt = Bcrypt(app)              # For Hashing the password 
db.init_app(app)



@app.route('/login', methods=['GET', 'POST'])   # Login route
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first() #Checks if the User exist in the Database
        if user and bcrypt.check_password_hash(user.password, password): 
            session['user'] = email
            session['username'] = user.username
            return redirect('/')   # If the user exist, redirect the user to the database
        else:
            flash('Invalid credentials. Please try again.')
            return redirect('/login')
    return render_template('login.html')


@app.route('/')      # Home Page Route
def index():
    if 'user' not in session:
        return redirect('/login')
    
   
    return render_template(
        'index.html',
        code=session.get('code', ''),
        suggestions=session.get('suggestions', ''),
        fixed_code=session.get('fixed_code', ''),
        input_method=session.get('input_method', 'text'),
        username=session.get('username', 'Guest')
    )
