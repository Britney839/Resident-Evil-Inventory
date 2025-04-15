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


@app.route('/list')
def show_collectibles():
    collectibles = [
        {'name': 'Acid Rounds', 'image': 'acid-rounds.png', 'description': 'Special ammunition used exclusively with Claire Redfields GM 79 grenade launcher.'},
        {'name': 'Bejeweled Box', 'image': 'bejeweled-box.png', 'description': 'A key item used in a puzzle to obtain a crucial object.'},
        {'name': 'Blue Herb', 'image': 'blue-herb.png', 'description': 'Cures poison status. Often used in combination with other herbs.'},
        {'name': 'Bolt Cutter', 'image': 'bolt-cutter.png', 'description': 'Used to cut through chains & padlocks, allowing access to new areas.'},
        {'name': 'Car Key', 'image': 'car-key.png', 'description': 'Opens police car trunk for weapon part'},
        {'name': 'Club Key', 'image': 'club-key.png', 'description': 'Unlocks club doors (Leon only).'},
        {'name': 'Combat Knife', 'image': 'combat-knife-infinite.png', 'description': 'Defensive melee weapon; can break after repeated use.'},
        {'name': 'Courtyard Key', 'image': 'courtyard-key.png', 'description': 'Key to the courtyard'},
        {'name': 'Detonator', 'image': 'detonator.png', 'description': 'Blows up C4 in the West Storage Room.'},
        {'name': 'Diamond Key', 'image': 'diamond-key.png', 'description': 'Unlocks diamond doors (Claire only)'},
        {'name': 'Electronic Gadget', 'image': 'electronic-gadget.png', 'description': 'Combine with Battery to create Detonator.'},
        {'name': 'First Aid Spray', 'image': 'first-aid-spray.png', 'description': 'Fully restores health.'},
        {'name': 'Flame Rounds', 'image': 'flame-rounds.jpg', 'description': 'Used with GM 79. Great against organic enemies.'},
        {'name': 'Flamethrower', 'image': 'flamethrower.png', 'description': 'Leon-exclusive weapon. Uses fuel to emit fire.'},
        {'name': 'Flash Grenade', 'image': 'flash-grenade.jpg', 'description': 'Temporarily blinds enemies. Stuns bosses. Can be defensive.'},
        {'name': 'Fuel', 'image': 'fuel.jpg', 'description': 'Used for the Flamethrower.'},
        {'name': 'Fuse (Main Hall)', 'image': 'fuse-main-hall.png', 'description': 'Restores power to West Office shutter.'},
        {'name': 'Green Herb', 'image': 'green-herb.png', 'description': 'Restores a small amount of health.'},
        {'name': 'Gunpowder', 'image': 'gunpowder.png', 'description': 'Craft Handgun Ammo.'},
        {'name': 'Gun Stock (Matilda)', 'image': 'gun-stock-matilda.png', 'description': 'Enables 3-round burst.'},
        {'name': 'Grenade', 'image': 'hand-grenade.png', 'description': 'High-damage explosive. Can be used defensively.'},
        {'name': 'Heart Key', 'image': 'heart-key.jpg', 'description': 'Unlocks heart doors (Claire only)'},
        {'name': 'High Capacity Mag (Matilda)', 'image': 'high-capacity-mag.jpg', 'description': 'Increases ammo capacity.'},
        {'name': 'High Grade Gunpowder (Yellow)', 'image': 'high-grade-gunpowder-yellow.png', 'description': 'Combine for Shotgun or Magnum ammo.'},
        {'name': 'High Grade Gunpowder (White)', 'image': 'white-high-grade-gunpowder.jpg', 'description': 'Combine for Submachine Gun ammo.'},
        {'name': 'High Powered Rounds (SLS 60)', 'image': 'high-powered-rounds-sls-60.png', 'description': 'Powerful ammo for Claires revolver.'},
        {'name': 'High Voltage Condenser (Spark Shot)', 'image': 'high-voltage-condenser-spark-shot.png', 'description': 'Reduces time between shots.'},
        {'name': 'Large Caliber Handgun Ammo', 'image': 'large-caliber-handgun-ammo.png', 'description': 'Heavy powered ammo for the heavier handguns.'},
        {'name': 'Large Gunpowder', 'image': 'large-gunpowder.jpg', 'description': 'Yields more ammo when crafting.'},
        {'name': 'Lightning Hawk', 'image': 'lightning-hawk.png', 'description': 'Leons Magnum. Very powerful, high-precision.'},
        {'name': 'Long Barrel (Lightning Hawk)', 'image': 'long-barrel-lightning-hawk.png', 'description': 'Increases power and accuracy.'},
        {'name': 'Matilda', 'image': 'matilda.jpg', 'description': 'Leons handgun. Can be upgraded to burst fire.'},
        {'name': 'Mixed Herb (G + R + B)', 'image': 'mixed-herb-grb.jpg', 'description': 'Fully heals, cures poison, and grants temporary defense.'},
        {'name': 'MQ-11', 'image': 'mq-11.png', 'description': 'Claires SMG. High rate of fire, good for groups.'},
        {'name': 'Muzzle Brake (Matilda)', 'image': 'muzzle-brake-matilda.jpg', 'description': 'Reduces recoil.'},
        {'name': 'Parking Garage Keycard', 'image': 'parking-garage-keycard.jpg'},
        {'name': 'Red Dot Sight', 'image': 'red-dot-sight.jpg', 'description': 'Improves aim.'},
        {'name': 'Red Herb', 'image': 'red-herb.png', 'description': 'No effect alone; combine with Green for stronger healing.'},
        {'name': 'Regulator (Flamethrower)', 'image': 'regulator-flamethrower.jpg', 'description': 'Controls fuel flow.'},
        {'name': 'Reinforced Frame (SLS 60)', 'image': 'reinforced-frame-sls-60.png', 'description': 'Allows high-powered rounds.'},
        {'name': 'Sewers Key', 'image': 'sewers-key.png', 'description': 'Opens door with key icon in Sewers.'},
        {'name': 'Shoulder Stock (GM-79)', 'image': 'shoulder-stock-gm-79.png', 'description': 'Reduces recoil and aim time.'},
        {'name': 'Spade Key', 'image': 'spade-key.png', 'description': 'Unlocks spade-marked doors (Leon & Claire).'},
        {'name': 'Speed Loader (SLS 60)', 'image': 'speed-loader-sls-60.jpg', 'description': 'Faster reloading.'},
        {'name': 'S.T.A.R.S Badge', 'image': 'stars-badge.png', 'description': 'USB drive to access S.T.A.R.S Armory. Doubles as hidden case key.'},
        {'name': 'Submachine Gun Ammo', 'image': 'submachine-gun-ammo.png', 'description': 'For the MQ-11.'},
        {'name': 'W-870', 'image': 'w-870.png', 'description': 'Leons shotgun. Effective at close range.'},
        {'name': 'Weapons Locker Keycard', 'image': 'weapons-locker-key-card.png', 'description': 'Opens gun locker (W-870 or GM-79).'},
        {'name': 'Wooden Boards', 'image': 'wooden-boards.png', 'description': 'Block windows to prevent zombie entry.'}]
    return render_template("list.html", collectibles=collectibles)

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
