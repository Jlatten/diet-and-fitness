from flask import Flask, jsonify, request

from google_sheets_integration import (
    add_grocery_item, 
    remove_grocery_item,
    add_inventory_item,
    remove_inventory_item,
    log_meal,
    log_workout,
    get_inventory,
    get_grocery_list,
    get_daily_tracking,
    get_weekly_tracking,
    get_fitness_daily_tracking,
    get_fitness_weekly_tracking
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Fitness and Diet GPT!'

# Add an item to the grocery list
@app.route('/add-grocery-item', methods=['GET'])
def add_grocery_item_route():
    item_name = request.args.get('item_name')
    quantity = request.args.get('quantity')
    category = request.args.get('category')
    priority = request.args.get('priority')

    try:
        add_grocery_item(item_name, quantity, category, priority)
        return jsonify({'status': 'success', 'message': f'Added {item_name} to the grocery list.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Remove an item from the grocery list
@app.route('/remove-grocery-item', methods=['GET'])
def remove_grocery_item_route():
    item_name = request.args.get('item_name')

    try:
        remove_grocery_item(item_name)
        return jsonify({'status': 'success', 'message': f'Removed {item_name} from the grocery list.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Add an item to the inventory list
@app.route('/add-inventory-item', methods=['GET'])
def add_inventory_item_route():
    item_name = request.args.get('item_name')
    quantity = request.args.get('quantity')
    category = request.args.get('category')
    expiration_date = request.args.get('expiration_date')

    try:
        add_inventory_item(item_name, quantity, category, expiration_date)
        return jsonify({'status': 'success', 'message': f'Added {item_name} to the inventory.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Remove an item from the inventory list
@app.route('/remove-inventory-item', methods=['GET'])
def remove_inventory_item_route():
    item_name = request.args.get('item_name')

    try:
        remove_inventory_item(item_name)
        return jsonify({'status': 'success', 'message': f'Removed {item_name} from the inventory list.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get the current inventory
@app.route('/inventory', methods=['GET'])
def get_inventory_route():
    try:
        inventory = get_inventory()
        return jsonify(inventory)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get the current grocery list
@app.route('/grocery-list', methods=['GET'])
def get_grocery_list_route():
    try:
        grocery_list = get_grocery_list()
        return jsonify(grocery_list)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get daily tracking data
@app.route('/daily-tracking', methods=['GET'])
def get_daily_tracking_route():
    try:
        data = get_daily_tracking()
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get weekly tracking data
@app.route('/weekly-tracking', methods=['GET'])
def get_weekly_tracking_route():
    try:
        data = get_weekly_tracking()
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get fitness daily tracking data
@app.route('/fitness-daily-tracking', methods=['GET'])
def get_fitness_daily_tracking_route():
    try:
        data = get_fitness_daily_tracking()
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get fitness weekly tracking data
@app.route('/fitness-weekly-tracking', methods=['GET'])
def get_fitness_weekly_tracking_route():
    try:
        data = get_fitness_weekly_tracking()
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Log a meal
@app.route('/log-meal', methods=['GET'])
def log_meal_route():
    try:
        log_meal(**request.args)
        return jsonify({'status': 'success', 'message': 'Meal logged successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Log a workout
@app.route('/log-workout', methods=['GET'])
def log_workout_route():
    try:
        log_workout(**request.args)
        return jsonify({'status': 'success', 'message': 'Workout logged successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

