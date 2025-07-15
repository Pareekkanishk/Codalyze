import os
import psycopg2
from flask import Flask, render_template, request, send_file, session, redirect, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from code_review import analyze_code, fix_code
from pdf_export import generate_pdf
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

@app.route('/register', methods=['GET', 'POST']) # Sign up page Route
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        raw_password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = email
        session['username'] = username
        return redirect('/')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


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
@app.route('/review', methods=['POST'])
def review():
    if 'user' not in session:
        return redirect('/login')

    code_text = ""
    input_method = request.form.get("inputMethod")

    if input_method == "text":
        code_text = request.form.get("codeEditor", "")
    elif input_method == "file":
        file = request.files.get("codeFile")
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code_text = f.read()

    suggestions = analyze_code(code_text)

    # Save to session
    session['code'] = code_text
    session['suggestions'] = suggestions
    session['input_method'] = input_method
    session.pop('fixed_code', None)

    return redirect('/')


@app.route('/fix', methods=['POST'])
def fix():
    if 'user' not in session:
        return redirect('/login')

    code = request.form.get("codeEditor", "")
    fixed_code = fix_code(code)

    # Update session to remove suggestions when fixed code is shown
    session['code'] = code
    session['fixed_code'] = fixed_code
    session['input_method'] = 'text'
    session.pop('suggestions', None)  # Hide suggestions when AI Fix is triggered

    return redirect('/')

@app.route('/export', methods=['POST'])
def export():
    if 'user' not in session:
        return redirect('/login')

    code = request.form.get("code", "")
    suggestions = request.form.get("suggestions", "")
    pdf_file = generate_pdf(code, suggestions)

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="codalyze_review.pdf",
        mimetype="application/pdf"
    )

# Clear session via JS for Refresh Button
@app.route("/clear", methods=["POST"])
def clear():
    session.pop("code", None)
    session.pop("suggestions", None)
    session.pop("fixed_code", None)
    session.pop("input_method", None)
    return '', 204

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
