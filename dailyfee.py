import time
import requests
import telebot
import jdatetime
import pytz
import json
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
    jalali_date_str = f"{jalali_date.year}/{jalali_date.month:02d}/{jalali_date.day:02d}"
    time_str = now.strftime("%H:%M")
    return f" {time_str} - {jalali_date_str}"

def send_to_telegram(message):
    """Send a message to the specified Telegram chat using the bot."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="HTML")
        print("Message sent to Telegram!")
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

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
    """
    Determine the emoji based on price change.
    Prices are first cast to float.
    Returns an up arrow if new > old, a down arrow if new < old,
    and an empty string if unchanged or if conversion fails.
    """
    try:
        # Convert values to float for proper comparison
        old_val = float(old)
        new_val = float(new)
    except (TypeError, ValueError):
        return ""
    
    if new_val > old_val:
        return " ⬆️"
    elif new_val < old_val:
        return " ⬇️"
    else:
        return ""

def fetch_prices():
    """Fetch gold and currency prices from the API."""
    try:
        gold_response = requests.get(GOLD_API_URL)
        gold_response.raise_for_status()
        gold_prices = gold_response.json()["data"]["prices"]

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
        # Convert to float and divide by 10 (as in your original code)
        number = float(number) / 10
        return "{:,.0f}".format(number)
    except ValueError:
        return number

def format_message(gold_prices, currency_prices):
    """
    Format a single message that shows the current prices with
    an emoji only when the price has changed compared to the previously stored price.
    """
    previous_prices = load_previous_prices()
    new_prices = {}

    jalali_datetime = get_current_jalali_datetime()
    message = f"<b>🗓 تاریخ و زمان:{jalali_datetime}</b>\n\n🏅 <b>قیمت طلا و ارز:</b>\n"

    # Define the labels for gold and currency items.
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

    # Process gold prices.
    for key, label in gold_labels.items():
        old_price = previous_prices.get(key)
        # Use .get("current") safely (if key or "current" is missing, new_price becomes None)
        new_price = gold_prices.get(key, {}).get("current")
        new_prices[key] = new_price
        emoji = ""
        # Only add emoji if both old and new prices exist
        if old_price is not None and new_price is not None:
            emoji = get_price_change_emoji(old_price, new_price)
        message += f"🔹 {label}: {format_number(new_price)} تومان{emoji}\n"

    # Process currency prices.
    for key, label in currency_labels.items():
        old_price = previous_prices.get(key)
        new_price = currency_prices.get(key, {}).get("current")
        new_prices[key] = new_price
        emoji = ""
        if old_price is not None and new_price is not None:
            emoji = get_price_change_emoji(old_price, new_price)
        message += f"🔹 {label}: {format_number(new_price)} تومان{emoji}\n"

    # Update the stored prices for the next comparison.
    save_previous_prices(new_prices)
    return message

def check_time_and_notify():
    """Check the time and send a message at 00, 15, 30, and 45 minutes past each hour."""
    tehran_tz = pytz.timezone("Asia/Tehran")
    
    while True:
        now = datetime.now(tehran_tz)
        hour, minute, weekday = now.hour, now.minute, now.weekday()
        
        # Send only between 9 AM and 8 PM and on specific weekdays (Saturday to Wednesday)
        if 9 <= hour < 21 and weekday in [0, 1, 2, 3, 6]:
            if minute in [0, 15, 30, 45]:
                gold_prices, currency_prices = fetch_prices()
                if gold_prices and currency_prices:
                    message = format_message(gold_prices, currency_prices)
                    send_to_telegram(message)
                    print(f"Message sent at {now.strftime('%H:%M:%S')} Tehran time")
        
        # Sleep until the start of the next minute.
        time.sleep(60 - now.second)

if __name__ == "__main__":
    check_time_and_notify()
