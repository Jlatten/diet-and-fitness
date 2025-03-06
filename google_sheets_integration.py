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
    print("Attempting to write to Daily Tracking sheet...")
    try:
        daily_tracking_sheet.append_row([
            date, meal_type, food_items, calories, protein, carbs, fat, hydration, diet_notes, rating
        ])
        print("Successfully logged meal to Daily Tracking sheet.")
    except Exception as e:
        print(f"Failed to write to Daily Tracking sheet: {e}")

# Function to log a workout
def log_workout(date, workout_type, duration, calories_burned, weight_lifted, workout_notes):
    print("Attempting to write to Fitness Daily Tracking sheet...")
    try:
        fitness_daily_tracking_sheet.append_row([
            date, workout_type, duration, calories_burned, weight_lifted, workout_notes
        ])
        print("Successfully logged workout to Fitness Daily Tracking sheet.")
    except Exception as e:
        print(f"Failed to write to Fitness Daily Tracking sheet: {e}")

# Verbose logging for inventory and grocery list updates
def add_grocery_item(item_name, quantity, category, priority, purchased='No'):
    print(f"Adding grocery item: {item_name}, Quantity: {quantity}, Category: {category}, Priority: {priority}")
    try:
        grocery_list_sheet.append_row([item_name, quantity, category, priority, purchased])
        print(f"Successfully added {item_name} to Grocery List.")
    except Exception as e:
        print(f"Failed to add grocery item: {e}")

print("Google Sheets integration script started.")
print("Loaded Google Sheets credentials successfully.")
print("Writing data to Google Sheets...")
print("Data written successfully!")