import telebot
from telebot import types
import yfinance as yf
import numpy as np

TOKEN = '7251044786:AAGOg7oUuLdVeM8O_wZWNr4fwPL-zCQbhoU'
bot = telebot.TeleBot(TOKEN)

# أزواج الكريبتو الأشهر
CRYPTO_PAIRS = [
    'BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','XRPUSDT','DOGEUSDT','ADAUSDT',
    'AVAXUSDT','TRXUSDT','LINKUSDT','MATICUSDT','DOTUSDT','LTCUSDT','SHIBUSDT'
]

# أزواج الفوركس والذهب الشهيرة
FOREX_PAIRS = [
    'XAUUSD','EURUSD','USDJPY','GBPUSD','USDCHF','AUDUSD','NZDUSD','USDCAD','EURGBP','EURJPY'
]

def luxalgo_analysis(symbol):
    try:
        yf_symbol = symbol.replace('USDT', '-USD').replace('XAUUSD', 'GC=F')
        data = yf.download(tickers=yf_symbol, period='7d', interval='15m')
        close = data['Close']
        price = float(close[-1])
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()
        trend = "صاعد" if ma20[-1] > ma50[-1] else "هابط"
        power = abs(ma20[-1] - ma50[-1]) / price
        support = min(close[-20:])
        resistance = max(close[-20:])
        action = "🚀 شراء قوي" if (trend == "صاعد" and price > ma20[-1]) else "📉 بيع محتمل" if (trend == "هابط" and price < ma20[-1]) else "🔍 ترقّب"
        tp = round(price * (1.008 if "شراء" in action else 0.992), 2)
        sl = round(price * (0.992 if "شراء" in action else 1.008), 2)
        msg = f"""🌟 [تحليل Ninja LuxAlgo-Style]  
⏳ الزوج: {symbol}
💰 السعر الحالي: {price}
📈 الاتجاه: {trend}  
🔥 قوة الاتجاه: {power:.3f}
📊 دعم: {support:.2f} | مقاومة: {resistance:.2f}
🟢 الإشارة: {action}
🎯 الهدف: {tp}
⛔ وقف الخسارة: {sl}
---
🤖 استراتيجية: LuxAlgo  
👤 المستخدم: {message_author}
🧑‍💻 المصمم: Mohammad (ChatGPT)
(تحليل لحظي من السوق الحقيقي. لا توجد إشارات وهمية)
"""
        return msg
    except Exception as e:
        return "⚠️ تعذر جلب التحليل الآن، جرب بعد قليل!"

# لوحة أزرار مقسمة مرتبة وصغيرة
def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=4)
    # كريبتو أولا
    crypto_rows = [types.InlineKeyboardButton(f"{s[:-4]}", callback_data=f"CR_{s}") for s in CRYPTO_PAIRS]
    forex_rows  = [types.InlineKeyboardButton(s, callback_data=f"FX_{s}") for s in FOREX_PAIRS]
    for i in range(0, len(crypto_rows), 4):
        markup.add(*crypto_rows[i:i+4])
    for i in range(0, len(forex_rows), 4):
        markup.add(*forex_rows[i:i+4])
    # خدمات إضافية
    markup.add(
        types.InlineKeyboardButton("🧠 إشارات AI", callback_data="AI"),
        types.InlineKeyboardButton("💎 VIP", callback_data="VIP")
    )
    markup.add(
        types.InlineKeyboardButton("📸 تحليل صورة", callback_data="PHOTO"),
        types.InlineKeyboardButton("🔄 تحديث", callback_data="REFRESH")
    )
    return markup

@bot.message_handler(commands=['start'])
def welcome(message):
    ninja_pic = 'https://i.imgur.com/z7wBXZg.png'  # صورة نينجا 3D (مثال)
    bot.send_photo(
        message.chat.id,
        ninja_pic,
        caption=f"""👑 أهلاً بك في بوت Ninja XAU GPT  
🔥 أقوى تحليل لحظي فوركس وكريبتو بنظام LuxAlgo  
اختر من الأزرار السريعة أو أرسل صورة شارت للتحليل  
👤 المستخدم: {message.from_user.first_name}
🧑‍💻 المصمم: Mohammad""",
        reply_markup=main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global message_author
    message_author = call.from_user.first_name if call.from_user else "User"
    if call.data.startswith("CR_"):
        symbol = call.data[3:]
        res = luxalgo_analysis(symbol)
        bot.edit_message_text(
            res, call.message.chat.id, call.message.message_id, reply_markup=main_keyboard()
        )
    elif call.data.startswith("FX_"):
        symbol = call.data[3:]
        res = luxalgo_analysis(symbol)
        bot.edit_message_text(
            res, call.message.chat.id, call.message.message_id, reply_markup=main_keyboard()
        )
    elif call.data == "AI":
        bot.edit_message_text(
            "🧠 إشارات الذكاء الاصطناعي:\nتحليل LuxAlgo-style لأي زوج.\nاختر عملة أو اطلب تحليل تلقائي.",
            call.message.chat.id, call.message.message_id, reply_markup=main_keyboard()
        )
    elif call.data == "VIP":
        bot.edit_message_text(
            "💎 VIP:\nتوصيات حصرية – سيتم ربطها بمصادر مباشرة قريباً.",
            call.message.chat.id, call.message.message_id, reply_markup=main_keyboard()
        )
    elif call.data == "PHOTO":
        bot.send_message(call.message.chat.id, "📸 أرسل صورة الشارت للتحليل...")
    elif call.data == "REFRESH":
        bot.edit_message_text(
            "🔄 تم التحديث! اختر زوج جديد أو خدمة إضافية.",
            call.message.chat.id, call.message.message_id, reply_markup=main_keyboard()
        )
    else:
        bot.answer_callback_query(call.id, "❗️اختر خدمة من القائمة.")

@bot.message_handler(content_types=['photo'])
def photo_handler(msg):
    bot.reply_to(msg, "📊 تم استلام الصورة! ميزة تحليل الشارت قيد التطوير...")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "⚡ أرسل /start لعرض القائمة أو استخدم الأزرار.")

if __name__ == '__main__':
    bot.infinity_polling()
