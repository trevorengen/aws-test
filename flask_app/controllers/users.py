from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register_input(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    if User.get_user({'email': data['email']}) != False:
        flash('User exists, please login.')
        return redirect('/')
    else:
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login_input(request.form):
        return redirect('/')
    data = {'email': request.form['email']}
    user = User.get_user(data)
    if not user:
        flash(u'Invalid email/password.', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(u'Invalid email/password.', 'login')
        return redirect('/')
    session['user_id'] = user.id 
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        user_id = session['user_id']
        user = User.get_user({'id': user_id})
        return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    del session['user_id']
    return redirect('/')