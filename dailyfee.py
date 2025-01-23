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

def format_message(gold_prices, currency_prices):
    """Format the message with Persian translations and emojis."""
    
    # Get the current Jalali date and time
    jalali_datetime = get_current_jalali_datetime()

    # Gold prices message
    gold_message = f"<b>🗓 تاریخ و زمان: {jalali_datetime}</b>\n\n🏅 <b>قیمت طلا:</b>\n"
    gold_message += f"🔹 مثقال: {format_number(gold_prices['mesghal']['current'])} تومان\n"
    gold_message += f"🔹 گرمی ۲۴ عیار: {format_number(gold_prices['geram24']['current'])} تومان\n"
    gold_message += f"🔹 گرمی ۱۸ عیار: {format_number(gold_prices['geram18']['current'])} تومان\n"
    gold_message += f"🔹 اونس جهانی: {format_number(gold_prices['ons']['current'])} دلار\n"
    gold_message += f"🔹 سکه امامی: {format_number(gold_prices['sekee_emami']['current'])} تومان\n"
    gold_message += f"🔹 سکه بهار آزادی: {format_number(gold_prices['seke_bahar']['current'])} تومان\n"
    gold_message += f"🔹 نیم‌سکه: {format_number(gold_prices['nim']['current'])} تومان\n"
    gold_message += f"🔹 ربع‌سکه: {format_number(gold_prices['rob']['current'])} تومان\n"
    gold_message += f"🔹 گرمی: {format_number(gold_prices['gerami']['current'])} تومان\n\n"

    # Important currencies message
    important_currency_message = f"<b>🗓 تاریخ و زمان: {jalali_datetime}</b>\n\n💱 <b>قیمت ارز (مهم):</b>\n"
    important_currency_message += f"💵 دلار آمریکا: {format_number(currency_prices['USD']['current'])} تومان\n"
    important_currency_message += f"💶 یورو: {format_number(currency_prices['EUR']['current'])} تومان\n"
    important_currency_message += f"💷 پوند انگلیس: {format_number(currency_prices['GBP']['current'])} تومان\n"
    important_currency_message += f"💴 ین ژاپن: {format_number(currency_prices['JPY']['current'])} تومان\n"
    important_currency_message += f"💴 دلار کانادا: {format_number(currency_prices['CAD']['current'])} تومان\n"
    important_currency_message += f"💵 دلار استرالیا: {format_number(currency_prices['AUD']['current'])} تومان\n"

    # Other currencies message (with 🔹 instead of flags)
    other_currency_message = f"<b>🗓 تاریخ و زمان: {jalali_datetime}</b>\n\n🌍 <b>قیمت ارز (دیگر):</b>\n"
    other_currency_message += f"🔹 درهم امارات: {format_number(currency_prices['AED']['current'])} تومان\n"
    other_currency_message += f"🔹 لیر ترکیه: {format_number(currency_prices['TRY']['current'])} تومان\n"
    other_currency_message += f"🔹 یوان چین: {format_number(currency_prices['CNY']['current'])} تومان\n"
    other_currency_message += f"🔹 کرون سوئد: {format_number(currency_prices['SEK']['current'])} تومان\n"
    other_currency_message += f"🔹 کرون دانمارک: {format_number(currency_prices['DKK']['current'])} تومان\n"
    other_currency_message += f"🔹 کرون نروژ: {format_number(currency_prices['NOK']['current'])} تومان\n"
    other_currency_message += f"🔹 ریال عربستان: {format_number(currency_prices['SAR']['current'])} تومان\n"
    other_currency_message += f"🔹 ریال قطر: {format_number(currency_prices['QAR']['current'])} تومان\n"
    other_currency_message += f"🔹 ریال عمان: {format_number(currency_prices['OMR']['current'])} تومان\n"
    other_currency_message += f"🔹 دینار عراق: {format_number(currency_prices['IQD']['current'])} تومان\n"
    other_currency_message += f"🔹 دلار هنگ‌کنگ: {format_number(currency_prices['HKD']['current'])} تومان\n"
    other_currency_message += f"🔹 رینگیت مالزی: {format_number(currency_prices['MYR']['current'])} تومان\n"
    other_currency_message += f"🔹 روبل روسیه: {format_number(currency_prices['RUB']['current'])} تومان\n"
    other_currency_message += f"🔹 لاری گرجستان: {format_number(currency_prices['GEL']['current'])} تومان\n"
    other_currency_message += f"🔹 بات تایلند: {format_number(currency_prices['THB']['current'])} تومان\n"
    other_currency_message += f"🔹 دلار سنگاپور: {format_number(currency_prices['SGD']['current'])} تومان\n"
    other_currency_message += f"🔹 منات آذربایجان: {format_number(currency_prices['AZN']['current'])} تومان\n"
    other_currency_message += f"🔹 درام ارمنستان: {format_number(currency_prices['AMD']['current'])} تومان\n"
    other_currency_message += f"🔹 روپیه هند: {format_number(currency_prices['INR']['current'])} تومان\n"
    other_currency_message += f"🔹 دلار نیوزلند: {format_number(currency_prices['NZD']['current'])} تومان\n"
    other_currency_message += f"🔹 افغانی افغانستان: {format_number(currency_prices['AFN']['current'])} تومان\n"
    other_currency_message += f"🔹 دینار بحرین: {format_number(currency_prices['BHD']['current'])} تومان\n"
    other_currency_message += f"🔹 لیر سوریه: {format_number(currency_prices['SYP']['current'])} تومان\n"
    other_currency_message += f"🔹 روپیه پاکستان: {format_number(currency_prices['PKR']['current'])} تومان\n"

    # Return all parts as separate messages
    return gold_message, important_currency_message, other_currency_message

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
    while True:
        now = datetime.now()
        minute = now.minute

        # Only proceed if it's 15, 30, 45, or 00 minutes
        if minute in [0, 15, 30, 45]:
            fetch_and_notify()
            print(f"Message sent at {now.strftime('%H:%M:%S')}")
        
        # Sleep until the next full minute
        time.sleep(60 - now.second)

if __name__ == "__main__":
    check_time_and_notify()
