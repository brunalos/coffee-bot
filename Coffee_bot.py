# import python modules

from dotenv import dotenv_values
import asyncio
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# get your token from an .env file
config = dotenv_values(".env")
token = config.get("TELEGRAM_TOKEN")

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

drink_type, intensity, size_selection, exit_choice = range(4)

# start the conversation
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hey, I am your coffee bot! Welcome to Strembucks!\n" 
        "Let's get your coffee preferences.\n"
        "What type of drink would you like?\n"
        "/coffee, /Espresso, /Long, Cappuccino, or Latte Macchiato?\n\n"
        "Select /cancel if you don't want to talk to me."
    )
    return drink_type

# stores the drink type and asks about how strong would like your coffee
async def drink_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    coffee_types = ['/coffee', '/espresso', '/long', 'cappuccino', 'latte macchiato']
    user_input = update.message.text.lower()

    if user_input in coffee_types:
        context.user_data['drink_type'] = user_input
        await update.message.reply_text(
            f"You've chosen {user_input}. How intense would you like your coffee?\nMild, medium, strong"
        )
        return intensity
    else:
        await update.message.reply_text(
            "Please select a valid drink type from the options below:\n"
            "Coffee, Espresso, Long, Cappuccino, or Latte Macchiato"
        )
        return drink_type

# stores the intensity and asks about the size of your drink
async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    intensity_types = ['mild', 'medium', 'strong']
    user_input = update.message.text.lower()

    if user_input in intensity_types:
        context.user_data['intensity'] = user_input
        await update.message.reply_text(
            "Great! Coffee's brewing! What's your preference: one cup or two?"
        )
        return size_selection
    else:
        await update.message.reply_text(
            "Please select a valid coffee intensity from the options below:\n"
            "Mild, medium, strong."
        )
        return intensity

# stores the size and exits 
async def size_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_size = ['one', 'two']
    user_input = update.message.text.lower()

    if user_input in reply_size:
        context.user_data['size'] = user_input
        order_details = "Alright, that's a {} {} {}! Your drinks will be ready shortly.".format(
            context.user_data.get('size', ''),
            context.user_data.get('intensity', ''),
            context.user_data.get('drink_type', '')
        )
        await update.message.reply_text(order_details)

        return exit_choice
    else: 
        await update.message.reply_text(
            "Please select a valid coffee size from the options below:\n "
            "One or two"
        )
        return size_selection


# stores the user input and end the conversation
async def exit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        'Goodbye! Enjoy your coffee!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# cancel and end the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        'Goodbye! Have a nice coffeeless day! ', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# run the bot
def main() -> None:
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            drink_type: [MessageHandler(filters.Regex('^coffee$|^espresso$|^long$|^cappuccino$|^latte macchiato$'), drink_type)],
            intensity: [MessageHandler(filters.Regex('^mild$|^medium$|^strong$'), intensity)],
            size_selection: [MessageHandler(filters.Regex('^one $|^two $'), size_selection)],
            exit_choice: [MessageHandler(filters.TEXT, exit_choice)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # Use asyncio to run the application
    # asyncio.run(application.run_polling(allowed_updates=Update.ALL_TYPES))

if __name__ == '__main__':
    main()
