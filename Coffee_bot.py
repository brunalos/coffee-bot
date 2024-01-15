# import python modules

from dotenv import dotenv_values
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

# Retrieve your bot token from a .env file.
config = dotenv_values(".env")
token = config.get("TELEGRAM_TOKEN")

# Enable logging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

drink_type, intensity, size_selection, exit_choice = range(4)

# Start the conversation.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Bot started by user: %s", update.message.from_user.id)
    await update.message.reply_text(
        "Hey, I am your coffee bot! Welcome to Strembucks!\n" 
        "What type of drink would you like?\n"
        "Coffee, Espresso, Long, Cappuccino, or Latte Macchiato?\n\n"
        "Select /cancel if you don't want to talk to me."
    )
    return select_drink_type

# Stores the user's selected drink type and prompts for their desired coffee strength.
async def select_drink_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    coffee_types = ['coffee', 'espresso', 'long', 'cappuccino', 'latte macchiato']
    user_input = update.message.text.lower()
    logger.info("User %s chose drink type: %s", update.message.from_user.id, user_input)

    if user_input in coffee_types:
        context.user_data['drink_type'] = user_input
        await update.message.reply_text(
            f"You've chosen {user_input}. How intense would you like your coffee?\nMild, medium, strong"
        )
        return intensity
    else:
        logger.warning("User %s provided an invalid drink type: %s", update.message.from_user.id, user_input)
        await update.message.reply_text(
            "Please select a valid drink type from the options below:\n"
            "Coffee, Espresso, Long, Cappuccino, or Latte Macchiato"
        )
        return select_drink_type

# Stores the user's desired coffee strength and prompts for their coffee size.
async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    intensity_types = ['mild', 'medium', 'strong']
    user_input = update.message.text.lower()
    logger.info("User %s chose intensity: %s", update.message.from_user.id, user_input)

    if user_input in intensity_types:
        context.user_data['intensity'] = user_input
        await update.message.reply_text(
            "Great! Coffee's brewing! What's your preference: one cup or two?"
        )
        return size_selection
    else:
        logger.warning("User %s provided an invalid intensity: %s", update.message.from_user.id, user_input)
        await update.message.reply_text(
            "Please select a valid coffee intensity from the options below:\n"
            "Mild, medium, strong."
        )
        return intensity

# Stores the user's desired coffee size and concludes the conversation.
async def size_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_size = ['one', 'two']
    user_input = update.message.text.lower()
    logger.info("User %s chose coffee size: %s", update.message.from_user.id, user_input)

    if user_input in reply_size:
        context.user_data['size'] = user_input
        order_details = "Alright, that's a {} {} {}! Your drink will be ready shortly.".format(
            context.user_data.get('size', ''),
            context.user_data.get('intensity', ''),
            context.user_data.get('drink_type', '')
        )
        await update.message.reply_text(
            f"{order_details}"
            "\nWould you like to order another drink? Reply with /drink_type."
            "\nIf you want to end this conversation, reply with /exit."
        )
    
        return exit_choice 

    else: 
        logger.warning("User %s provided an invalid coffee size: %s", update.message.from_user.id, user_input)
        await update.message.reply_text(
            "Please select a valid coffee size from the options below:\n"
            "One or two"
        )
        return size_selection


# Handler for the /drink_type command
async def drink_type_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Sure! What type of drink would you like?\n"
        "Coffee, Espresso, Long, Cappuccino, or Latte Macchiato?"
    )
    return select_drink_type 

# Concludes the conversation.
async def exit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        'Goodbye! Enjoy your coffee!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Cancels and concludes the conversation.
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        'Goodbye! Have a nice coffeeless day!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Run the bot
def main() -> None:
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('drink_type', drink_type_command)  
        ],
        states={
            select_drink_type: [MessageHandler(filters.TEXT, select_drink_type)],
            intensity: [MessageHandler(filters.TEXT, intensity)],
            size_selection: [MessageHandler(filters.TEXT, size_selection)],
            exit_choice: [CommandHandler('exit', exit_choice), MessageHandler(filters.TEXT, exit_choice)],
            cancel: [CommandHandler('cancel', cancel), MessageHandler(filters.TEXT, cancel)]
        },
        fallbacks=[CommandHandler('cancel', cancel), MessageHandler(filters.TEXT, cancel)]
    )

    application.add_handler(conv_handler)

    # Run the bot until the user interrupts with Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()