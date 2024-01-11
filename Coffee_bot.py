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

config = dotenv_values(".env")
token = config.get("TELEGRAM_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

drink_type, intensity, size_selection, exit_choice = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Welcome to Strembucks! Hey, I am your coffee bot! Let's get your coffee preferences.")
    return drink_type

async def drink_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Coffee', 'Espresso', 'Long', 'Cappuccino', 'Latte Macchiato']]

    await update.message.reply_text(
        'What type of drink would you like? '
        'Coffee, Espresso, Long, Cappuccino, or Latte Macchiato? '
        'Send /cancel to stop talking to me.\n\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Coffee, Espresso, Long, Cappuccino, or Latte Macchiato?'
        ),
    )

    return intensity

async def intensity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Mild', 'Medium', 'Strong']]
    user = update.message.from_user
    logger.info("Drink type %s: %s", user.first_name, update.message.text)
    context.user_data['drink_type'] = update.message.text
    await update.message.reply_text(
        'How intense are we going with the coffee today? '
        'Mild, Medium, or Strong? ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Mild, Medium, or Strong?'
        ),
    )

    return size_selection

async def size_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['one cup', 'two cups']]
    user = update.message.from_user
    context.user_data['intensity'] = update.message.text
    await update.message.reply_text(
        'Coffee\'s brewing! One cup or two, what\'s your preference?'
        'one cup or two cups? ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='one cup or two cups?'
        ),
    )

    return exit_choice

async def exit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data['size'] = update.message.text
    order_details = 'Alright, that\'s a {} {} {} for {}! Your drinks will be ready shortly.'.format(
            context.user_data.get('size', ''),
            context.user_data.get('intensity', ''),
            context.user_data.get('drink_type', ''),
            context.user_data.get('name', '')
        )
    await update.message.reply_text(order_details)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        'GoodBye! Have a nice coffeeless day', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

    
def main() -> None:
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            drink_type: [MessageHandler(filters.Regex('^Coffee$|^Espresso$|^Long$|^Cappuccino$|^Latte Macchiato$'), drink_type)],
            intensity: [MessageHandler(filters.Regex('^Mild$|^Medium$|^Strong$'), intensity)],
            size_selection: [MessageHandler(filters.Regex('^one cup$|^two cups$'), size_selection)],
            exit_choice: [MessageHandler(filters.TEXT, exit_choice)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
      
      