


import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Define the scope
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

# Authenticate with the JSON credentials using json.loads
creds = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS')),
    scopes=scope
)

# Connect to Google Sheets
client = gspread.authorize(creds)

# Open the Diet Tracking spreadsheet by URL
diet_spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1PDpRYdsZzf9gW-3r-PYHJtHncvKPezNAquAmBwXmD0E/edit?usp=sharing')

# Access specific sheets in the Diet Tracking spreadsheet by name
daily_tracking_sheet = diet_spreadsheet.worksheet('Daily Tracking')
weekly_tracking_sheet = diet_spreadsheet.worksheet('Weekly Tracking')
inventory_sheet = diet_spreadsheet.worksheet('Inventory')
grocery_list_sheet = diet_spreadsheet.worksheet('Grocery List')

# Open the Fitness Tracking spreadsheet by URL
fitness_spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Os9BBhujsM1N3HIGjn73D1auRtBk4_VbWyxWEAVkng0/edit?usp=sharing')

# Access specific sheets in the Fitness Tracking spreadsheet by name
fitness_daily_tracking_sheet = fitness_spreadsheet.worksheet('Daily Tracking')
fitness_weekly_tracking_sheet = fitness_spreadsheet.worksheet('Weekly Tracking')

# Example of adding a row to the Daily Tracking sheet for diet with rating
daily_tracking_sheet.append_row([
    datetime.now().strftime('%Y-%m-%d'),
    'Lunch',
    'Salmon Salad',
    500, 30, 20, 10, '64oz', 'High protein', 'Liked'
])

# Example of adding a workout to the Fitness Tracking sheet with feedback
fitness_daily_tracking_sheet.append_row([
    datetime.now().strftime('%Y-%m-%d'),
    'Strength Training',
    60, 300, '50 lbs', 'Felt strong, could increase weight next time'
])

