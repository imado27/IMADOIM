from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageFilter
import io

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("تأثيرات على الصور", callback_data='apply_effects')],
        [InlineKeyboardButton("مساعدة", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا! أرسل صورة أو فيديو، أو اختر تأثيرًا من الأزرار أدناه:", reply_markup=reply_markup)

# Function to handle user requests for effects
def apply_effects(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("أرسل صورة أو فيديو لتطبيق التأثيرات عليها!")

# Function to handle /help command
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("أرسل صورة أو فيديو ليتم تطبيق تأثيرات مختلفة عليها. يمكنك أيضًا اختيار تأثيرات من خلال الأزرار.")

# Function to apply filter on image
def apply_filter(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Get the last photo (largest)
        photo = update.message.photo[-1].get_file()
        photo.download("temp_image.jpg")
        
        # Open the image and apply a filter (Gaussian Blur as an example)
        img = Image.open("temp_image.jpg")
        img = img.filter(ImageFilter.GaussianBlur(radius=5))  # Example effect
        
        # Save and send the modified image
        img.save("modified_image.jpg")
        update.message.reply_photo(photo=open("modified_image.jpg", 'rb'))
    
    elif update.message.video:
        # Process the video (Example: sending back as is)
        video = update.message.video.get_file()
        video.download("temp_video.mp4")
        
        # Modify video as needed (e.g., apply watermark, overlay, etc.)
        update.message.reply_video(video=open("temp_video.mp4", 'rb'))

# Function to handle inline button callbacks
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Handle button presses
    if query.data == 'apply_effects':
        query.edit_message_text(text="أرسل صورة أو فيديو لتطبيق التأثيرات عليها!")
    elif query.data == 'help':
        query.edit_message_text(text="أرسل صورة أو فيديو ليتم تطبيق تأثيرات مختلفة عليها. يمكنك أيضًا اختيار تأثيرات من خلال الأزرار.")

# Main function to start the bot
def main() -> None:
    # Replace with your own Bot API Token
    updater = Updater("8116664785:AAEPSvpTGmWCXaWKwu8IkrNAjjEswL5JiVg", use_context=True)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.photo, apply_filter))
    dp.add_handler(MessageHandler(Filters.video, apply_filter))
    dp.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
