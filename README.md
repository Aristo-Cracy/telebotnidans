# AESL Answer Key Telegram Bot

This bot takes a Test ID (NID) from Telegram and returns an HTML answer key file.

## Setup

1. Replace `YOUR_BOT_TOKEN` in `bot.py` or use environment variables.
2. Add allowed user IDs in `ALLOWED_USERS` list.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the bot:

```bash
python bot.py
```

## Deploy to Render

1. Push this repo to GitHub.
2. Create a new **Background Worker** on [https://render.com](https://render.com).
3. Set your environment variable `TOKEN` to your Telegram bot token.
4. Done!
