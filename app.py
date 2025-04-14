from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import uuid


app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.secret_key = 'raccoon-city'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 #this provides app configuration for the maximum file size the user can upload.
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"


file_save_location = "static/images"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_file():
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    return f"data/{user_id}"


@app.route('/', methods=['GET'])
def index():
    if 'inventory' not in session:
        session['inventory'] = []
    print(session.get("inventory"))
    return render_template('index.html', inventory=session['inventory'], file_location=file_save_location)

@app.route('/inventory')
def inventory():
    if 'inventory' not in session:
        session['inventory'] = []
    return render_template("inventory.html", inventory=session['inventory'], file_location=file_save_location)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        return render_template("add_item.html")
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        usage = request.form['usage']
        file = request.files['image']

        if not name or not description or not usage or not file:
            flash('All fields are required.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            item = {
                'id': str(uuid.uuid4()),
                'name': name,
                'description': description,
                'usage': usage,
                'image': unique_filename
            }

            inventory = session.get('inventory', [])
            inventory.append(item)
            session['inventory'] = inventory
            session.modified = True
            return redirect(url_for('inventory'))
        else:
            flash('Invalid image file.')
            return redirect(request.url)

@app.route('/remove/<string:item_id>')
def remove_item(item_id):
    inventory = session.get('inventory', [])
    updated_inventory = []
    for item in inventory:
        if item['id'] == item_id:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], item['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
            continue
        updated_inventory.append(item)

    session['inventory'] = updated_inventory
    session.modified = True
    return redirect(url_for('inventory'))


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
