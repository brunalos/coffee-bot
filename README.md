# Coffee Bot 

## Overview

Coffee Bot (@strembucks_bot) is a Telegram bot designed to streamline your coffee preferences. 

## Files

- **Coffee_bot.py**: The main script for the Telegram bot.
- **.env.example**: Example file for retrieving your bot token. Please rename it to `.env` and fill in the necessary information.

## Prerequisites

Before getting started with Coffee Bot, ensure you have the following in place:

1. **Telegram Bot Created with @BotFather:**
   - Visit [Telegram's BotFather](https://core.telegram.org/bots/features#botfather) for instructions on creating a new bot.

2. **Python and Python Modules:**
   - Python 3.9.7
   - Required Python modules:
     - `dotenv` (version 1.0.0)
     - `python-telegram-bot` (version 20.7)

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/coffee-bot.git
   cd coffee-bot
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Bot Token:**
   - Rename `.env.example` to `.env`.
   - Open `.env` and replace `YOUR_BOT_TOKEN` with the actual token obtained from BotFather.

6. **Run the Bot:**
   ```bash
   python Coffee_bot.py
   ```

Now, your Coffee Bot should be up and running on Telegram! ☕

For any additional assistance or troubleshooting, refer to the [Telegram Bot documentation](https://core.telegram.org/bots) and the respective Python module documentation.

