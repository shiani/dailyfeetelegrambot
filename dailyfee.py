import time
import requests
import telebot
import jdatetime
import pytz
from datetime import datetime

# Replace with your actual API code and Telegram Bot details
API_CODE = "029c97dd2ac8eeec238bdeb4ad17e3e1"  # Replace with your API code
GOLD_API_URL = f"http://nerkh-api.ir/api/{API_CODE}/gold/"
CURRENCY_API_URL = f"http://nerkh-api.ir/api/{API_CODE}/currency/"
TELEGRAM_BOT_TOKEN = "7427661797:AAFdk8nsNwhpzbjtSIyowe2cuII1Y4mJad0"
TELEGRAM_CHAT_ID = "-1002412585293"

# Initialize the Telebot instance
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_current_jalali_datetime():
    """Get the current date and time in Tehran timezone and convert to Jalali."""
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    jalali_date = jdatetime.date.fromgregorian(date=now.date())
    # Format the Jalali date as year/month/day
    jalali_date_str = f"{jalali_date.year}/{jalali_date.month:02d}/{jalali_date.day:02d}"
    time_str = now.strftime("%H:%M")  # Format time as HH:MM:SS
    return f" {time_str} - {jalali_date_str}"


def send_to_telegram(message):
    """Send a message to the specified Telegram chat using the bot."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="HTML")
        print("Message sent to Telegram!")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def fetch_prices():
    """Fetch gold and currency prices from the API."""
    try:
        # Fetch gold prices
        gold_response = requests.get(GOLD_API_URL)
        gold_response.raise_for_status()
        gold_prices = gold_response.json()["data"]["prices"]

        # Fetch currency prices
        currency_response = requests.get(CURRENCY_API_URL)
        currency_response.raise_for_status()
        currency_prices = currency_response.json()["data"]["prices"]

        return gold_prices, currency_prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return None, None
    
def format_number(number):
    """Format the number with commas as thousands separators."""
    try:
        # Ensure the number is treated as a number (int or float)
        number = float(number) / 10
        return "{:,.0f}".format(number)  # This will add commas and remove decimals
    except ValueError:
        # If it can't be converted to a number, return the number as is
        return number

import json
import time
import requests
import pytz
from datetime import datetime

def load_previous_prices():
    """Load previous prices from a file."""
    try:
        with open("previous_prices.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_previous_prices(prices):
    """Save current prices to a file."""
    with open("previous_prices.json", "w") as file:
        json.dump(prices, file)

def get_price_change_emoji(old, new):
    """Determine the emoji based on price change."""
    if old is None:
        return ""
    elif new > old:
        return " ⬆️"
    elif new < old:
        return " ⬇️"
    else:
        return ""

def fetch_prices():
    """Fetch gold and currency prices from the API."""
    try:
        # Fetch gold prices
        gold_response = requests.get(GOLD_API_URL)
        gold_response.raise_for_status()
        gold_prices = gold_response.json()["data"]["prices"]

        # Fetch currency prices
        currency_response = requests.get(CURRENCY_API_URL)
        currency_response.raise_for_status()
        currency_prices = currency_response.json()["data"]["prices"]

        return gold_prices, currency_prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return None, None

def format_message(gold_prices, currency_prices):
    """Format message with price changes and emojis."""
    previous_prices = load_previous_prices()
    new_prices = {}

    jalali_datetime = get_current_jalali_datetime()
    message = f"<b>🗓 تاریخ و زمان: {jalali_datetime}</b>\n\n🏅 <b>قیمت طلا و ارز:</b>\n"

    # Gold prices
    gold_labels = {
        "mesghal": "مثقال",
        "geram24": "گرمی ۲۴ عیار",
        "geram18": "گرمی ۱۸ عیار",
        "ons": "اونس جهانی",
        "sekee_emami": "سکه امامی",
        "seke_bahar": "سکه بهار آزادی",
        "nim": "نیم‌سکه",
        "rob": "ربع‌سکه",
        "gerami": "گرمی"
    }
    for key, label in gold_labels.items():
        old_price = previous_prices.get(key)
        new_price = gold_prices.get(key, {}).get("current")
        new_prices[key] = new_price
        emoji = get_price_change_emoji(old_price, new_price)
        message += f"🔹 {label}: {format_number(new_price)} تومان{emoji}\n"

    # Currency prices
    currency_labels = {
        "USD": "دلار آمریکا",
        "EUR": "یورو",
        "GBP": "پوند انگلیس",
        "JPY": "ین ژاپن",
        "CAD": "دلار کانادا",
        "AUD": "دلار استرالیا",
        "AED": "درهم امارات",
        "TRY": "لیر ترکیه",
        "CNY": "یوان چین",
        "SEK": "کرون سوئد",
        "DKK": "کرون دانمارک",
        "NOK": "کرون نروژ",
        "SAR": "ریال عربستان",
        "QAR": "ریال قطر",
        "OMR": "ریال عمان",
        "IQD": "دینار عراق",
        "HKD": "دلار هنگ‌کنگ",
        "MYR": "رینگیت مالزی",
        "RUB": "روبل روسیه",
        "GEL": "لاری گرجستان",
        "THB": "بات تایلند",
        "SGD": "دلار سنگاپور",
        "AZN": "منات آذربایجان",
        "AMD": "درام ارمنستان",
        "INR": "روپیه هند",
        "NZD": "دلار نیوزلند",
        "AFN": "افغانی افغانستان",
        "BHD": "دینار بحرین",
        "SYP": "لیر سوریه",
        "PKR": "روپیه پاکستان"
    }
    for key, label in currency_labels.items():
        old_price = previous_prices.get(key)
        new_price = currency_prices.get(key, {}).get("current")
        new_prices[key] = new_price
        emoji = get_price_change_emoji(old_price, new_price)
        message += f"🔹 {label}: {format_number(new_price)} تومان{emoji}\n"

    save_previous_prices(new_prices)
    return message

def check_time_and_notify():
    """Check the time and send message at 15, 30, 45, and 00 minute of each hour."""
    tehran_tz = pytz.timezone("Asia/Tehran")
    
    while True:
        now = datetime.now(tehran_tz)
        hour, minute, weekday = now.hour, now.minute, now.weekday()
        
        if 9 <= hour < 21 and weekday in [0, 1, 2, 3, 6]:  # Saturday (6) to Wednesday (3)
            if minute in [0, 15, 30, 45]:
                gold_prices, currency_prices = fetch_prices()
                if gold_prices and currency_prices:
                    message = format_message(gold_prices, currency_prices)
                    send_to_telegram(message)
                    print(f"Message sent at {now.strftime('%H:%M:%S')} Tehran time")
        
        time.sleep(60 - now.second)

if __name__ == "__main__":
    check_time_and_notify()

def fetch_and_notify():
    """Fetch prices and send the formatted message to Telegram."""
    gold_prices, currency_prices = fetch_prices()
    if gold_prices and currency_prices:
        gold_message, important_currency_message, other_currency_message = format_message(gold_prices, currency_prices)
        
        # Send messages to Telegram
        send_to_telegram(gold_message)
        send_to_telegram(important_currency_message)
        send_to_telegram(other_currency_message)
    else:
        pass

def check_time_and_notify():
    """Check the time and send message at 15, 30, 45, and 00 minute of each hour."""
    tehran_tz = pytz.timezone("Asia/Tehran")
    
    while True:
        now = datetime.now(tehran_tz)
        hour, minute, weekday = now.hour, now.minute, now.weekday()
        
        # Check if the time is between 9 AM and 8 PM (21 is excluded) and it's Saturday-Wednesday (0-3)
        if 9 <= hour < 21 and weekday in [0, 1, 2, 3, 6]:  # Saturday (6) to Wednesday (3)
            if minute in [0, 15, 30, 45]:
                fetch_and_notify()
                print(f"Message sent at {now.strftime('%H:%M:%S')} Tehran time")
        
        # Sleep until the next full minute
        time.sleep(60 - now.second)

if __name__ == "__main__":
    check_time_and_notify()
