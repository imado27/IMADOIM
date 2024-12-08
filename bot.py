from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# الدالة لبدء البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "مرحبًا! أرسل /send لتحديد التوكن، الشات آي دي، والرسالة."
    )

# الدالة لجمع المعلومات
def send(update: Update, context: CallbackContext):
    update.message.reply_text("أرسل التوكن الخاص بالبوت:")
    context.user_data['step'] = 'token'

# معالجة الرسائل
def handle_message(update: Update, context: CallbackContext):
    step = context.user_data.get('step')

    if step == 'token':
        context.user_data['token'] = update.message.text
        update.message.reply_text("أرسل الآن Chat ID:")
        context.user_data['step'] = 'chat_id'

    elif step == 'chat_id':
        context.user_data['chat_id'] = update.message.text
        update.message.reply_text("أرسل الرسالة التي تريد إرسالها:")
        context.user_data['step'] = 'message'

    elif step == 'message':
        token = context.user_data.get('token')
        chat_id = context.user_data.get('chat_id')
        message = update.message.text

        # إرسال الرسالة
        send_message(token, chat_id, message)
        update.message.reply_text("تم إرسال الرسالة بنجاح!")
        context.user_data.clear()

# دالة إرسال الرسالة
def send_message(token, chat_id, message):
    import requests
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

# إعداد البوت
def main():
    updater = Updater("7672599367:AAHH6rZbSHyOhkhOtNEM90AZA1TXrhAKJb4", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
