from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
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
import os
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication setup
users = {"admin": os.getenv('API_PASSWORD')}

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users[username]:
        logger.info(f"Authenticated user: {username}")
        return username

# ======================
# ROUTES WITH AUTH & VALIDATION
# ======================

@app.route('/')
def home():
    return 'Welcome to the Fitness and Diet GPT!'

@app.route('/add-grocery-item', methods=['GET'])
@auth.login_required
def add_grocery_item_route():
    try:
        required_params = ['item_name', 'quantity']
        missing = [p for p in required_params if not request.args.get(p)]
        if missing:
            return jsonify({'status': 'error', 'message': f'Missing parameters: {", ".join(missing)}'}), 400

        add_grocery_item(
            request.args.get('item_name'),
            request.args.get('quantity'),
            request.args.get('category'),
            request.args.get('priority')
        )
        return jsonify({'status': 'success', 'message': f'Added {request.args.get("item_name")} to grocery list'})
    except Exception as e:
        logger.error(f"Add grocery error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/remove-grocery-item', methods=['GET'])
@auth.login_required
def remove_grocery_item_route():
    try:
        if not request.args.get('item_name'):
            return jsonify({'status': 'error', 'message': 'Missing item_name parameter'}), 400
            
        remove_grocery_item(request.args.get('item_name'))
        return jsonify({'status': 'success', 'message': f'Removed {request.args.get("item_name")} from grocery list'})
    except Exception as e:
        logger.error(f"Remove grocery error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/add-inventory-item', methods=['GET'])
@auth.login_required
def add_inventory_item_route():
    try:
        required_params = ['item_name', 'quantity']
        missing = [p for p in required_params if not request.args.get(p)]
        if missing:
            return jsonify({'status': 'error', 'message': f'Missing parameters: {", ".join(missing)}'}), 400

        add_inventory_item(
            request.args.get('item_name'),
            request.args.get('quantity'),
            request.args.get('category'),
            request.args.get('expiration_date')
        )
        return jsonify({'status': 'success', 'message': f'Added {request.args.get("item_name")} to inventory'})
    except Exception as e:
        logger.error(f"Inventory add error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/remove-inventory-item', methods=['GET'])
@auth.login_required
def remove_inventory_item_route():
    try:
        if not request.args.get('item_name'):
            return jsonify({'status': 'error', 'message': 'Missing item_name parameter'}), 400
            
        remove_inventory_item(request.args.get('item_name'))
        return jsonify({'status': 'success', 'message': f'Removed {request.args.get("item_name")} from inventory'})
    except Exception as e:
        logger.error(f"Inventory remove error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/inventory', methods=['GET'])
@auth.login_required
def get_inventory_route():
    try:
        return jsonify(get_inventory())
    except Exception as e:
        logger.error(f"Inventory fetch error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/grocery-list', methods=['GET'])
@auth.login_required
def get_grocery_list_route():
    try:
        return jsonify(get_grocery_list())
    except Exception as e:
        logger.error(f"Grocery list error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/log-meal', methods=['GET'])
@auth.login_required
def log_meal_route():
    try:
        required_params = ['date', 'meal_type', 'food_items']
        missing = [p for p in required_params if not request.args.get(p)]
        if missing:
            return jsonify({'status': 'error', 'message': f'Missing parameters: {", ".join(missing)}'}), 400

        log_meal(**request.args)
        return jsonify({'status': 'success', 'message': 'Meal logged successfully'})
    except Exception as e:
        logger.error(f"Meal logging error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/log-workout', methods=['GET'])
@auth.login_required
def log_workout_route():
    try:
        required_params = ['date', 'workout_type', 'exercise_name', 'sets_reps_weight', 'duration', 'calories_burned', 'workout_notes']
        missing = [p for p in required_params if not request.args.get(p)]
        if missing:
            return jsonify({'status': 'error', 'message': f'Missing parameters: {", ".join(missing)}'}), 400

        log_workout(
            request.args.get('date'),
            request.args.get('workout_type'),
            request.args.get('exercise_name'),
            request.args.get('sets_reps_weight'),
            request.args.get('duration'),
            request.args.get('calories_burned'),
            request.args.get('workout_notes')
        )
        return jsonify({'status': 'success', 'message': 'Workout logged successfully'})
    except Exception as e:
        logger.error(f"Workout logging error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
@app.route('/daily-tracking', methods=['GET'])
@auth.login_required
def get_daily_tracking_route():
    try:
        data = get_daily_tracking()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Daily tracking error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/weekly-tracking', methods=['GET'])
@auth.login_required
def get_weekly_tracking_route():
    try:
        data = get_weekly_tracking()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Weekly tracking error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)