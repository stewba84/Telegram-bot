from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
from collections import defaultdict
from flask import Flask
from threading import Thread
import os

# Flask server to keep Railway app alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_web).start()

# Dictionary to store contract counts
contract_counts = defaultdict(int)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /add <contract>, /list, or /logo")

def add_contract(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /add <contract>")
        return
    address = context.args[0]
    contract_counts[address] += 1
    update.message.reply_text(f"✅ Added: {address}\nTotal: {contract_counts[address]}")

def list_contracts(update: Update, context: CallbackContext):
    if not contract_counts:
        update.message.reply_text("No contracts added yet.")
        return
    msg = "\n".join([f"{addr} — {count}" for addr, count in contract_counts.items()])
    update.message.reply_text(msg)

def send_logo(update: Update, context: CallbackContext):
    try:
        with open("logo.png", "rb") as img:
            update.message.reply_photo(photo=InputFile(img), caption="Here is the logo!")
    except:
        update.message.reply_text("❌ Could not send the logo (logo.png not found).")

def main():
    keep_alive()
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ Error: BOT_TOKEN environment variable not set.")
        return
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_contract))
    dp.add_handler(CommandHandler("list", list_contracts))
    dp.add_handler(CommandHandler("logo", send_logo))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
