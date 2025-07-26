import telebot
from telebot import types
import requests
import yfinance as yf

# توكن البوت الجديد
TOKEN = "7251044786:AAGOg7oUuLdVeM8O_wZWNr4fwPL-zCQbhoU"
bot = telebot.TeleBot(TOKEN)

# أزواج الكريبتو الرئيسية
CRYPTO_SYMBOLS = {
    "BTCUSDT": "Bitcoin",
    "ETHUSDT": "Ethereum",
    "BNBUSDT": "BNB",
    "SOLUSDT": "Solana",
    "XRPUSDT": "XRP",
    "DOGEUSDT": "Dogecoin",
    "ADAUSDT": "Cardano"
}

# أزواج الفوركس والذهب الأساسية
FOREX_SYMBOLS = {
    "XAUUSD": "Gold",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "USDCAD": "USD/CAD",
    "AUDUSD": "AUD/USD",
    "NZDUSD": "NZD/USD"
}

# خريطة رموز ياهو
YAHOO_SYMBOLS = {
    "XAUUSD": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "USDCAD": "CAD=X",
    "AUDUSD": "AUDUSD=X",
    "NZDUSD": "NZDUSD=X"
}

def get_crypto_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        r = requests.get(url, timeout=5)
        price = float(r.json()['price'])
        return price
    except:
        return None

def get_forex_price(symbol):
    if symbol not in YAHOO_SYMBOLS:
        return None
    data = yf.Ticker(YAHOO_SYMBOLS[symbol]).history(period="1d", interval="1m")
    if not data.empty:
        price = float(data["Close"].iloc[-1])
        return price
    return None

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for k, v in CRYPTO_SYMBOLS.items():
        markup.add(types.InlineKeyboardButton(f"{v} ({k})", callback_data=f"CRYPTO_{k}"))
    for k, v in FOREX_SYMBOLS.items():
        markup.add(types.InlineKeyboardButton(f"{v} ({k})", callback_data=f"FOREX_{k}"))
    markup.add(types.InlineKeyboardButton("🧠 إشارات الذكاء الاصطناعي", callback_data="AI_SIGNALS"))
    markup.add(types.InlineKeyboardButton("📸 تحليل صورة شارت", callback_data="IMAGE_AI"))
    markup.add(types.InlineKeyboardButton("🚀 العملات الرائجة", callback_data="TRENDING"))
    markup.add(types.InlineKeyboardButton("📰 آخر الأخبار", callback_data="NEWS"))
    markup.add(types.InlineKeyboardButton("💎 VIP", callback_data="VIP"))
    return markup

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "👑 مرحباً بك في PhantomTrader500!\n\nاختر نوع التحليل أو العملة من الأزرار أو أرسل رمز مباشرة مثل BTCUSDT أو XAUUSD.",
        reply_markup=main_menu()
    )

@bot.message_handler(content_types=['text'])
def text_handler(msg):
    symbol = msg.text.replace("/", "").upper().strip()
    if symbol in CRYPTO_SYMBOLS:
        price = get_crypto_price(symbol)
        if price:
            bot.reply_to(msg, f"💰 سعر {CRYPTO_SYMBOLS[symbol]} الآن ({symbol}):\n${price:,.2f}")
        else:
            bot.reply_to(msg, f"❌ تعذّر جلب سعر {symbol} الآن.")
    elif symbol in FOREX_SYMBOLS:
        price = get_forex_price(symbol)
        if price:
            bot.reply_to(msg, f"💰 سعر {FOREX_SYMBOLS[symbol]} الآن ({symbol}):\n${price:,.2f}")
        else:
            bot.reply_to(msg, f"❌ تعذّر جلب سعر {symbol} الآن.")
    else:
        bot.reply_to(msg, "❗️أرسل رمز زوج صحيح أو اختر من الأزرار /start")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("CRYPTO_"):
        symbol = call.data.split("_")[1]
        price = get_crypto_price(symbol)
        if price:
            bot.edit_message_text(
                f"💰 سعر {CRYPTO_SYMBOLS[symbol]} الآن ({symbol}):\n${price:,.2f}",
                call.message.chat.id, call.message.message_id,
                reply_markup=main_menu()
            )
        else:
            bot.answer_callback_query(call.id, f"❌ تعذّر جلب سعر {symbol}", show_alert=True)
    elif call.data.startswith("FOREX_"):
        symbol = call.data.split("_")[1]
        price = get_forex_price(symbol)
        if price:
            bot.edit_message_text(
                f"💰 سعر {FOREX_SYMBOLS[symbol]} الآن ({symbol}):\n${price:,.2f}",
                call.message.chat.id, call.message.message_id,
                reply_markup=main_menu()
            )
        else:
            bot.answer_callback_query(call.id, f"❌ تعذّر جلب سعر {symbol}", show_alert=True)
    elif call.data == "AI_SIGNALS":
        bot.edit_message_text("🤖 إشارات AI:\nشراء BTCUSDT عند الدعم ٦٦٥٠٠ بهدف ٧٠٠٠٠ (مثال تجريبي)\n\n🧠 تطوير الإشارات الذكية قيد العمل...", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "IMAGE_AI":
        bot.send_message(call.message.chat.id, "📸 أرسل صورة الشارت لتحليلها...")
    elif call.data == "TRENDING":
        bot.edit_message_text("🚀 العملات الرائجة حالياً:\n- BTCUSDT\n- ETHUSDT\n- SOLUSDT\n- DOGEUSDT\n\n(بيانات تجريبية، سيتم جلب البيانات الحية في التحديثات القادمة)", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "NEWS":
        bot.edit_message_text("📰 آخر الأخبار:\n- السوق يتحرك بشكل إيجابي!\n- ترقب لقرار الفائدة الأمريكي...\n\n(نظام الأخبار الحقيقي سيتم ربطه قريباً)", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif call.data == "VIP":
        bot.edit_message_text("💎 خدمة VIP الحصرية:\nراسل الدعم للانضمام لقائمة كبار المتداولين 👑", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "❗️اختر خدمة من القائمة.")

@bot.message_handler(content_types=['photo'])
def photo_handler(msg):
    bot.reply_to(msg, "📊 تم استلام الصورة! ميزة تحليل الشارت قيد التطوير...")

# تشغيل البوت
if __name__ == "__main__":
    print("🤖 PhantomTrader500 Bot يعمل الآن...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
