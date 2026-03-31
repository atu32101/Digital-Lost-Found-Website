from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, current_app
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lostfound_secret_key_change_in_production'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

DATA_FILE = 'data.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', items=data, logged_in=is_logged_in())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'student' and password == 'pass123':
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out!', 'info')
    return redirect(url_for('index'))

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if not is_logged_in():
        flash('Please log in to add item!', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']  # 'lost' or 'found'
        location = request.form['location']
        date = request.form['date']
        contact = request.form['contact']
        
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                image_filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        data = load_data()
        item = {
            'id': len(data) + 1,
            'title': title,
            'description': description,
            'category': category,
            'location': location,
            'date': date,
            'contact': contact,
            'image': image_filename
        }
        data.append(item)
        save_data(data)
        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_item.html')

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    data = load_data()
    item = next((i for i in data if i['id'] == item_id), None)
    if not item:
        flash('Item not found!', 'error')
        return redirect(url_for('index'))
    return render_template('item_detail.html', item=item)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
