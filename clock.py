#clock.py
import time

def get_time():
    """Returns current time formatted as HH:MM:SS AM/PM"""
    return time.strftime('%I:%M:%S %p')

def get_date():
    """Returns current date formatted like: Day, Month #, Year"""
    return time.strftime('%A, %B %d, %Y')