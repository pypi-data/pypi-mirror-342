from datetime import datetime, timedelta, date
import pytz
from zoneinfo import ZoneInfo
import uuid
from werkzeug.security import generate_password_hash
import re
import random
import string
import os
import inspect

def help():
    functions_list = [name for name, obj in inspect.getmembers(__import__(__name__)) if inspect.isfunction(obj)]
    print("Available functions in this module:")
    for func in functions_list:
        print(f"- {func}")

def get_countries():
    """
    Returns countries as a list in alphabetical order. 
    Example: ['Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina']
    """
    countries = [
        'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina',
        'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
        'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
        'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon',
        'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros',
        'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Democratic Republic of the Congo',
        'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
        'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France',
        'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea',
        'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
        'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
        'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
        'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives',
        'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia',
        'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
        'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea',
        'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama',
        'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania',
        'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
        'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
        'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
        'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname',
        'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
        'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda',
        'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
        'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
    ]
    return countries

def get_currencies():
    """
    Return a list of currencies as strings with symbols.
    Example: ['Euro (€)', 'Pound (£)']
    """
    currencies = [
        'Euro (€)', 
        'Pound (£)', 
        'US Dollar ($)', 
        'Yen (¥)', 
        'Australian Dollar (A$)', 
        'Canadian Dollar (C$)', 
        'Swiss Franc (CHF)', 
        'Chinese Yuan (¥)', 
        'Hong Kong Dollar (HK$)', 
        'Swedish Krona (kr)', 
        'Norwegian Krone (kr)', 
        'Singapore Dollar (S$)', 
        'Mexican Peso (Mex$)', 
        'Indian Rupee (₹)', 
        'Russian Ruble (₽)', 
        'Turkish Lira (₺)', 
        'South African Rand (R)', 
        'New Zealand Dollar (NZ$)', 
        'South Korean Won (₩)', 
        'Brazilian Real (R$)'
    ]

    return currencies

def get_payment_terms():
    """
    Return a list of common payment terms.
    Example: ['Prepayment', 'Cash on Delivery (COD)', "Bill of Exchange"]
    """
    payment_terms = [
        'Prepayment', 
        'Cash on Delivery (COD)', 
        'Letter of Credit (LC)', 
        'Open Account', 
        'Consignment', 
        'Advance Payment', 
        'Net 30', 
        'Net 60', 
        'Net 90', 
        'Documents Against Payment (DAP)', 
        'Documents Against Acceptance (DAA)', 
        'Cash in Advance (CIA)', 
        'Cash Before Shipment (CBS)', 
        'Cash on Shipment (COS)', 
        'Partial Payment', 
        'Telegraphic Transfer (T/T)', 
        'Bill of Exchange', 
        'Cash Against Documents (CAD)'
    ]

    return payment_terms

def get_shipping_metrics():
    """
    Return a list of common shipping metrics
    Example: ['Euro pallet (1200mm x 800mm)', 'Block pallet (1200mm x 1000mm)', 'LDM']
    """
    shipping_metrics = ['Euro pallet (1200mm x 800mm)', 'Block pallet (1200mm x 1000mm)', 'LDM'] 
    return shipping_metrics

def get_current_timestamp(timezone="Europe/Amsterdam"):
    """
    Returns current time in default AMS timezone as ISO string for DB comparison.
    This is used for EU/AMS operation
    """
    try:
        tz = pytz.timezone(timezone)
    except (pytz.UnknownTimeZoneError, AttributeError):
        tz = pytz.UTC

    return datetime.now(tz).isoformat()

def add_business_hours(start: datetime, hours: int) -> datetime:
    """
    This functions is used mainly for showing proper expiry dates. 
    In case the expiry dates span through a weekend it adds the weekend hours to the total in order to 'exclude them'

    As an example:
    A timestamp is generated on Friday 08:00 AM
    Expiry is set to 72 hours
    Hours of validity is Friday 08:00 AM + 72 (standard expiry) + 48h to account for Satruday and Sunday.

    It takes the first argument as a datetime stamp and the second as the expiry hours as an integer. 
    """
    current = start
    added = 0
    while added < hours:
        current += timedelta(hours=1)
        if current.weekday() < 5:  # Mon–Fri
            added += 1
    return current

def get_user_timestamp(user_timezone):
    """
    Returns a date-time stamp based on the user's timezone. 
    The only argument it takes is the timezone, which is stored in the users.db / users table
    This value is globally stored is session upon login as session['user_timezone']
    For AMS the timezone info looks like this: 'Europe/Amsterdam'
    
    An example usecase:
    creation_timestamp = get_user_timestamp(session['user_timezone'])
    returns: '2025-03-31 19:00:36'
    To store in SQL use TIMESTAMP field.

    Fallback mechanism:
    is the user's timezone is not recognised the function returns standard UTC timestamp.

    """
    try:
        user_tz = pytz.timezone(user_timezone)
    except pytz.UnknownTimeZoneError:
        user_tz = pytz.UTC

    return datetime.now(user_tz).strftime('%Y-%m-%d %H:%M:%S')

def generate_uuid():
    id = uuid.uuid4()
    return id

def generate_hashed_passqord(password):
    """
    It takes original password as an argument and returns the hashed version
    """
    hashed_passowrd = generate_password_hash(password)
    return hashed_passowrd

def get_seasonal_message(today=None):
    """
    Generates seasonal message based on the current date.
    It takes no argument and it used direectly in the email generation function
    """
    if not today:
        today = date.today()

    year = today.year
    if date(year, 12, 20) <= today <= date(year, 12, 31):
        return "Wishing you a warm and joyful holiday season and a happy new year!"
    elif date(year, 1, 1) <= today <= date(year, 1, 7):
        return "Wishing you a successful and inspiring start to the new year!"
    elif date(year, 3, 29) <= today <= date(year, 4, 2):
        return "Wishing you a relaxing and sunny Easter weekend!"
    elif date(year, 4, 27) == today:
        return "Enjoy the celebrations this King's Day!"
    elif date(year, 5, 5) == today:
        return "Wishing you a meaningful Liberation Day!"
    elif date(year, 5, 9) <= today <= date(year, 5, 12):
        return "Hope you enjoy the long weekend!"
    elif date(year, 5, 19) <= today <= date(year, 5, 21):
        return "Wishing you a peaceful Whit Monday!"
    elif date(year, 6, 15) <= today <= date(year, 8, 31):
        return "Hope you’re enjoying the summer and recharging well!"
    elif date(year, 11, 30) <= today <= date(year, 12, 5):
        return "Wishing you a cozy and festive Sinterklaas season!"
    elif date(year, 10, 15) <= today <= date(year, 10, 22):
        return "Hope you’re enjoying a well-deserved autumn break!"
    else:
        return "Wishing you a wonderful day!"
    
def get_today_day():
    """
    Returns today's day as for example: 'Wednesday'
    """
    return datetime.datetime.today().strftime('%A')

def validate_email(email: str) -> bool:
    """
    Validates an email address using regex.
    Returns True if valid, False if not.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def get_weekday_number(date: datetime) -> int:
    """
    Returns the day of the week as a number: Monday is 0, Sunday is 6.
    """
    return date.weekday()

def get_first_day_of_month(year: int, month: int) -> date:
    """
    Returns the first day of a specified month.
    """
    return date(year, month, 1)

def get_random_color() -> str:
    """
    Returns a random color in hexadecimal format.
    """
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def is_weekend(date: datetime) -> bool:
    """
    Returns True if the given date is a weekend (Saturday or Sunday), False otherwise.
    """
    return date.weekday() >= 5

def generate_unique_filename(filename: str) -> str:
    """
    Returns a unique filename using a UUID and the original file extension.
    """
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    return f"{unique_id}.{extension}"

def extract_domain_from_email(email: str) -> str:
    """
    Extract the domain from an email address.
    """
    return email.split('@')[-1]

def get_day_of_year(date: date) -> int:
    """
    Returns the day of the year (1 to 365 or 366).
    """
    return date.timetuple().tm_yday

def get_file_size(file_path: str) -> str:
    """
    Returns the size of the file at the given path as a human-readable string.
    """
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def generate_random_string(length: int = 8) -> str:
    """
    Generates a random alphanumeric string of a specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def get_time_difference(start_time: datetime, end_time: datetime) -> timedelta:
    """
    Returns the difference between two datetime objects as a timedelta object.
    """
    return end_time - start_time

def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """
    Converts a datetime from one timezone to another.
    Arguments:
        dt: The datetime object to convert.
        from_tz: The timezone to convert from (e.g., 'Europe/Amsterdam').
        to_tz: The timezone to convert to (e.g., 'Asia/Tokyo').
    Returns:
        The converted datetime.
    """
    try:
        from_timezone = pytz.timezone(from_tz)
        to_timezone = pytz.timezone(to_tz)
        dt_with_tz = from_timezone.localize(dt)
        return dt_with_tz.astimezone(to_timezone)
    except pytz.UnknownTimeZoneError:
        raise ValueError("Invalid timezone specified.")
    
def get_days_in_month(year: int, month: int) -> int:
    """
    Returns the number of days in a given month of a specific year.
    """
    from calendar import monthrange
    return monthrange(year, month)[1]

def get_age(birthdate: date) -> int:
    """
    Returns the age based on the birthdate.
    """
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age
