import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the scope
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
if not credentials_json:
    raise ValueError("GOOGLE_SHEETS_CREDENTIALS environment variable not set.")

creds = Credentials.from_service_account_info(
    json.loads(credentials_json),
    scopes=scope
)

client = gspread.authorize(creds)

# Connect to Google Sheets
diet_spreadsheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1PDpRYdsZzf9gW-3r-PYHJtHncvKPezNAquAmBwXmD0E/edit'
)

fitness_spreadsheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1Os9BBhujsM1N3HIGjn73D1auRtBk4_VbWyxWEAVkng0/edit'
)

# Access specific sheets
daily_tracking_sheet = diet_spreadsheet.worksheet('Daily Tracking')
weekly_tracking_sheet = diet_spreadsheet.worksheet('Weekly Tracking')
inventory_sheet = diet_spreadsheet.worksheet('Inventory')
grocery_list_sheet = diet_spreadsheet.worksheet('Grocery List')

fitness_daily_tracking_sheet = fitness_spreadsheet.worksheet('Daily Tracking')
fitness_weekly_tracking_sheet = fitness_spreadsheet.worksheet('Weekly Tracking')

# Function to log a meal
def log_meal(date, meal_type, food_items, calories, protein, carbs, fat, hydration, diet_notes, rating):
    print(f"Attempting to log meal: {meal_type} on {date}")
    daily_tracking_sheet.append_row([
        date, meal_type, food_items, calories, protein, carbs, fat, hydration, diet_notes, rating
    ])
    print("Meal logged successfully!")

# Function to log a workout
def log_workout(date, workout_type, exercise_name, sets_reps_weight, duration, calories_burned, workout_notes):
    print(f"Attempting to log workout: {exercise_name} ({workout_type}) on {date}")
    fitness_daily_tracking_sheet.append_row([
        date, workout_type, exercise_name, sets_reps_weight, duration, calories_burned, workout_notes
    ])
    print("Workout logged successfully!")

# Function to get current daily and weekly tracking data

def get_daily_tracking():
    print("Retrieving daily tracking data")
    return daily_tracking_sheet.get_all_records()

def get_weekly_tracking():
    print("Retrieving weekly tracking data")
    return weekly_tracking_sheet.get_all_records()

def get_fitness_daily_tracking():
    print("Retrieving fitness daily tracking data")
    return fitness_daily_tracking_sheet.get_all_records()

def get_fitness_weekly_tracking():
    print("Retrieving fitness weekly tracking data")
    return fitness_weekly_tracking_sheet.get_all_records()

# Function to get inventory and grocery list
def get_inventory():
    print("Retrieving inventory data")
    return inventory_sheet.get_all_records()

def get_grocery_list():
    print("Retrieving grocery list data")
    return grocery_list_sheet.get_all_records()

# Functions to add and remove items from grocery and inventory lists
def add_grocery_item(item_name, quantity, category, priority, purchased='No'):
    print(f"Adding grocery item: {item_name}")
    grocery_list_sheet.append_row([item_name, quantity, category, priority, purchased])
    print(f"Grocery item '{item_name}' added successfully")

def remove_grocery_item(item_name):
    print(f"Attempting to remove grocery item: {item_name}")
    cell = grocery_list_sheet.find(item_name)
    if cell:
        grocery_list_sheet.delete_rows(cell.row)
        print(f"Successfully removed grocery item: {item_name}")
    else:
        print(f"Grocery item '{item_name}' not found.")

def add_inventory_item(item_name, quantity, category, expiration_date=None):
    print(f"Adding inventory item: {item_name}")
    inventory_sheet.append_row([item_name, quantity, category, expiration_date or ''])
    print(f"Inventory item '{item_name}' added successfully")

def remove_inventory_item(item_name):
    print(f"Attempting to remove inventory item: {item_name}")
    cell = inventory_sheet.find(item_name)
    if cell:
        inventory_sheet.delete_rows(cell.row)
        print(f"Successfully removed inventory item: {item_name}")
    else:
        print(f"Inventory item '{item_name}' not found.")

print("Google Sheets integration script started.")

print("Loaded Google Sheets credentials successfully.")

print("Writing data to Google Sheets...")

print("Data written successfully!")