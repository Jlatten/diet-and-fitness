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
    'https://docs.google.com/spreadsheets/d/1PDpRYdsZzf9gW-3r-PYHJtHncvKPezNAquAmBwXmD0E/edit?usp=sharing'
)

fitness_spreadsheet = client.open_by_url(
    'https://docs.google.com/spreadsheets/d/1Os9BBhujsM1N3HIGjn73D1auRtBk4_VbWyxWEAVkng0/edit?usp=sharing'
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
    daily_tracking_sheet.append_row([
        date, meal_type, food_items, calories, protein, carbs, fat, hydration, diet_notes, rating
    ])

# Function to log a workout
def log_workout(date, workout_type, duration, calories_burned, weight_lifted, workout_notes):
    fitness_daily_tracking_sheet.append_row([
        date, workout_type, duration, calories_burned, weight_lifted, workout_notes
    ])

# Function to get current daily and weekly tracking data
def get_daily_tracking():
    return daily_tracking_sheet.get_all_records()

def get_weekly_tracking():
    return weekly_tracking_sheet.get_all_records()

def get_fitness_daily_tracking():
    return fitness_daily_tracking_sheet.get_all_records()

def get_fitness_weekly_tracking():
    return fitness_weekly_tracking_sheet.get_all_records()

# Function to get inventory and grocery list
def get_inventory():
    return inventory_sheet.get_all_records()

def get_grocery_list():
    return grocery_list_sheet.get_all_records()

# Functions to add and remove items from grocery and inventory lists
def add_grocery_item(item_name, quantity, category, priority, purchased='No'):
    grocery_list_sheet.append_row([item_name, quantity, category, priority, purchased])

def remove_grocery_item(item_name):
    cell = grocery_list_sheet.find(item_name)
    if cell:
        grocery_list_sheet.delete_rows(cell.row)

def add_inventory_item(item_name, quantity, category, expiration_date=None):
    inventory_sheet.append_row([item_name, quantity, category, expiration_date or ''])

def remove_inventory_item(item_name):
    cell = inventory_sheet.find(item_name)
    if cell:
        inventory_sheet.delete_rows(cell.row)
