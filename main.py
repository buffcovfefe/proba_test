import os
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

# Enable necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Allow bot to read messages

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Disable default help command

# Function to scrape BluePanel data using BeautifulSoup
def get_player_data(nick):
    url = f"https://bluepanel.bugged.ro/profile/{nick}"

    # Fake a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://google.com",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"❌ Failed to access the page. Status Code: {response.status_code}")
        return "N/A", "N/A", "N/A", "N/A"

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        faction = soup.select_one("div.profile-stat div:nth-of-type(1)").text.strip()
        playing_hours = soup.select_one("div.profile-stat div:nth-of-type(2)").text.strip()
        warnings = soup.select_one("div.profile-stat div:nth-of-type(3)").text.strip()
        faction_warns = soup.select_one("div.profile-stat div:nth-of-type(4)").text.strip()
    except AttributeError:
        faction, playing_hours, warnings, faction_warns = "N/A", "N/A", "N/A", "N/A"

    return faction, playing_hours, warnings, faction_warns

# Discord Command for !parere nick
@bot.command()
async def parere(ctx, nick: str = None):
    """Fetches data from BluePanel using BeautifulSoup"""

    if not nick:
        await ctx.send("⚠️ Format greșit! Folosește comanda astfel:\n```!parere [nick]```", delete_after=5)
        return  

    await ctx.send(f"🔎 Caut informații despre **{nick}**...")

    # Fetch player data
    faction, playing_hours, warnings, faction_warns = get_player_data(nick)

    # Send the formatted response in Discord
    message = await ctx.send(f"""📢 **Părere despre {nick}**
🔗 **Profil:** [Click aici](https://bluepanel.bugged.ro/profile/{nick})
🏛️ **Facțiune:** {faction}
⏳ **Ore jucate:** {playing_hours}
⚠️ **Avertismente:** {warnings}
🚨 **Faction Warns:** {faction_warns}
🛡️ Merită în clan?""")

    # Add reactions for voting
    try:
        await message.add_reaction("✅")  
        await message.add_reaction("❌")  
    except discord.Forbidden:
        await ctx.send("⚠️ Nu am permisiunea să adaug reacții!", delete_after=5)

# Bot Ready Event
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    bot.add_command(parere)  # Force-load the command

# Run the bot
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN is missing. Make sure it's set in Koyeb Secrets!")

bot.run(TOKEN)
