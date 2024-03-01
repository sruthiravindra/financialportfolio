from datetime import datetime
import pandas as pd

# Define a function to format keys
def format_key_to_month_year(key):
    # Example: Convert keys to month and year format
    try:
        # Create a Timestamp object
        timestamp = pd.Timestamp(key)

        # Convert Timestamp object to string
        timestamp_string = timestamp.strftime('%Y-%m-%d')

        # Use strptime() with the string representation of the Timestamp
        datetime_object = datetime.strptime(timestamp_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_datetime_format(string):
    try:
        datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
