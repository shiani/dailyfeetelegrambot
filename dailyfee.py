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
    """Save current (displayed) prices to a file."""
    with open("previous_prices.json", "w") as file:
        json.dump(prices, file)

def format_number(number):
    """
    Format the number with commas as thousands separators.
    The API raw number is divided by 10 before formatting.
    """
    try:
        number = float(number) / 10
        return "{:,.0f}".format(number)
    except (ValueError, TypeError):
        return number


def format_message(gold_prices, currency_prices):
    """
    Format a message showing the prices.
    For each price, we calculate the displayed price (raw_value/10 rounded down to an int)
    and compare it with the previously stored displayed value.
    An emoji is added only if the displayed value has changed.
    """
    previous_prices = load_previous_prices()
    new_prices = {}

    jalali_datetime = get_current_jalali_datetime()
    message = f"<b>🗓 تاریخ و زمان:{jalali_datetime}</b>\n\n🏅 <b>قیمت طلا و ارز:</b>\n"

    gold_labels = {
        "geram18": "گرمی ۱۸ عیار",
        "geram24": "گرمی ۲۴ عیار",
        "sekee_emami": "سکه امامی",
        "seke_bahar": "سکه بهار آزادی",
        "nim": "نیم‌سکه",
        "rob": "ربع‌سکه",
        "gerami": "گرمی",
        "mesghal": "مثقال",
        "ons": "اونس جهانی",
    }

    # Define proper emojis for gold items.
    # You can change these as you see fit.
    gold_emoji_map = {
        "geram18": "🥇",
        "geram24": "🥇",
        "sekee_emami": "🪙",
        "seke_bahar": "🪙",
        "nim": "🪙",
        "rob": "🪙",
        "gerami": "💰",
        "mesghal": "💎",
        "ons": "⚖️",
    }

    important_currency_labels = {
        "USD": "دلار آمریکا",
        "EUR": "یورو",
        "GBP": "پوند انگلیس",
        "CAD": "دلار کانادا",
        "AUD": "دلار استرالیا",
    }

    other_currency_labels = {
        "BHD": "دینار بحرین",
        "OMR": "ریال عمان",
        "SGD": "دلار سنگاپور",
        "AZN": "منات آذربایجان",
        "NZD": "دلار نیوزلند",
        "GEL": "لاری گرجستان",
        "QAR": "ریال قطر",
        "AED": "درهم امارات",
        "SAR": "ریال عربستان",
        "MYR": "رینگیت مالزی",
        "DKK": "کرون دانمارک",
        "CNY": "یوان چین",
        "HKD": "دلار هنگ‌کنگ",
        "SEK": "کرون سوئد",
        "NOK": "کرون نروژ",
        "THB": "بات تایلند",
        "TRY": "لیر ترکیه",
        "AFN": "افغانی افغانستان",
        "INR": "روپیه هند",
        "RUB": "روبل روسیه",
        "PKR": "روپیه پاکستان",
        "AMD": "درام ارمنستان",
        "IQD": "دینار عراق",
        "SYP": "لیر سوریه",
    }
    
    # Define proper emojis for currency items using country flags when applicable.
    currency_emojis = {
        "USD": "\u200F🇺🇸",
        "EUR": "\u200F🇪🇺",
        "GBP": "\u200F🇬🇧",
        "CAD": "\u200F🇨🇦",
        "AUD": "\u200F🇦🇺",
        "AED": "\u200F🇦🇪",
        "TRY": "\u200F🇹🇷",
        "CNY": "\u200F🇨🇳",
        "SEK": "\u200F🇸🇪",
        "DKK": "\u200F🇩🇰",
        "NOK": "\u200F🇳🇴",
        "SAR": "\u200F🇸🇦",
        "QAR": "\u200F🇶🇦",
        "OMR": "\u200F🇴🇲",
        "IQD": "\u200F🇮🇶",
        "HKD": "\u200F🇭🇰",
        "MYR": "\u200F🇲🇾",
        "GEL": "\u200F🇬🇪",
        "THB": "\u200F🇹🇭",
        "SGD": "\u200F🇸🇬",
        "AZN": "\u200F🇦🇿",
        "INR": "\u200F🇮🇳",
        "NZD": "\u200F🇳🇿",
        "AFN": "\u200F🇦🇫",
        "BHD": "\u200F🇧🇭",
        "RUB": "\u200F🇷🇺",
        "PKR": "\u200F🇵🇰",
        "AMD": "\u200F🇦🇲",
        "SYP": "\u200F🇸🇾",
    }

    # Process gold prices.
    for key, label in gold_labels.items():
        raw_new_price = gold_prices.get(key, {}).get("current")
        try:
            new_display = int(float(raw_new_price) / 10)
        except (TypeError, ValueError):
            new_display = None

        old_display = previous_prices.get(key)
        if old_display is not None:
            try:
                old_display = int(old_display)
            except (ValueError, TypeError):
                old_display = None

        change_emoji = ""
        if old_display is not None and new_display is not None:
            if new_display > old_display:
                change_emoji = " ⬆️"
            elif new_display < old_display:
                change_emoji = " ⬇️"

        line_emoji = gold_emoji_map.get(key, "💰")
        message += f"{line_emoji} {label}: {format_number(raw_new_price)} تومان{change_emoji}\n"
        new_prices[key] = new_display
    message += "\n"

    for key, label in important_currency_labels.items():
        raw_new_price = currency_prices.get(key, {}).get("current")
        try:
            new_display = int(float(raw_new_price) / 10)
        except (TypeError, ValueError):
            new_display = None

        old_display = previous_prices.get(key)
        if old_display is not None:
            try:
                old_display = int(old_display)
            except (ValueError, TypeError):
                old_display = None

        change_emoji = ""
        if old_display is not None and new_display is not None:
            if new_display > old_display:
                change_emoji = " ⬆️"
            elif new_display < old_display:
                change_emoji = " ⬇️"

        line_emoji = currency_emojis.get(key, "💱")
        message += f"{line_emoji} {label}: {format_number(raw_new_price)} تومان{change_emoji}\n"
        new_prices[key] = new_display

    message += "\n"
    for key, label in other_currency_labels.items():
        raw_new_price = currency_prices.get(key, {}).get("current")
        try:
            new_display = int(float(raw_new_price) / 10)
        except (TypeError, ValueError):
            new_display = None

        old_display = previous_prices.get(key)
        if old_display is not None:
            try:
                old_display = int(old_display)
            except (ValueError, TypeError):
                old_display = None

        change_emoji = ""
        if old_display is not None and new_display is not None:
            if new_display > old_display:
                change_emoji = " ⬆️"
            elif new_display < old_display:
                change_emoji = " ⬇️"
        line_emoji = currency_emojis.get(key, "💱")
        message += f"{line_emoji} {label}: {format_number(raw_new_price)} تومان{change_emoji}\n"
        new_prices[key] = new_display
    save_previous_prices(new_prices)
    return message


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

def check_time_and_notify():
    """Check the time and send a message at 00, 15, 30, and 45 minutes past each hour."""
    tehran_tz = pytz.timezone("Asia/Tehran")
    
    while True:
        now = datetime.now(tehran_tz)
        hour, minute, weekday = now.hour, now.minute, now.weekday()
        
        # Send only between 9 AM and 8 PM and on Saturday to Wednesday (weekday 6,0,1,2,3)
        if 9 <= hour < 21:
            if minute in [0, 15, 30, 45]:
                gold_prices, currency_prices = fetch_prices()
                if gold_prices and currency_prices:
                    message = format_message(gold_prices, currency_prices)
                    send_to_telegram(message)
                    print(f"Message sent at {now.strftime('%H:%M:%S')} Tehran time")
        
        time.sleep(60 - now.second)

if __name__ == "__main__":
    check_time_and_notify()
