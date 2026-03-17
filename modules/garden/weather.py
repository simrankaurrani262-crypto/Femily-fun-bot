"""
/weather command - Check weather
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random
import logging

logger = logging.getLogger(__name__)

WEATHER_EVENTS = [
    {
        "emoji": "☀️",
        "name": "Sunny",
        "effect": "+20% crop growth",
        "growth_bonus": 1.2
    },
    {
        "emoji": "🌧️",
        "name": "Rainy",
        "effect": "+50% crop growth",
        "growth_bonus": 1.5
    },
    {
        "emoji": "⛈️",
        "name": "Stormy",
        "effect": "-30% crop growth",
        "growth_bonus": 0.7
    },
    {
        "emoji": "🌤️",
        "name": "Cloudy",
        "effect": "Normal growth",
        "growth_bonus": 1.0
    },
    {
        "emoji": "❄️",
        "name": "Snowy",
        "effect": "-50% crop growth",
        "growth_bonus": 0.5
    },
    {
        "emoji": "🌈",
        "name": "Rainbow",
        "effect": "+100% crop growth",
        "growth_bonus": 2.0
    },
]

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check weather"""
    weather = random.choice(WEATHER_EVENTS)
    
    weather_text = f"""
<b>🌦️ WEATHER FORECAST</b>

{weather['emoji']} <b>{weather['name']}</b>

<b>Effect on Crops:</b>
{weather['effect']}

Growth Multiplier: {weather['growth_bonus']}x

Use /garden to see how weather affects your crops.
"""
    
    await update.message.reply_text(weather_text, parse_mode="HTML")
    logger.info(f"Weather: {weather['name']}")

weather_handler = CommandHandler('weather', weather_command)