import discord
from discord.ext import commands
import sqlite3
import requests
from bs4 import BeautifulSoup
import asyncio
import re
import json

# Load configuration from config.json
with open("config/config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]  # Discord bot token from config file
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Create SQLite database tables if not already created
def create_tables():
    conn = sqlite3.connect('data/bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS capcodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        capcode TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
        guild_id INTEGER PRIMARY KEY,
        alert_channel INTEGER,
        mention_role INTEGER
    )''')

    conn.commit()
    conn.close()

create_tables()

# Fetch pager data from the website
def fetch_latest_page():
    URL = "https://mazzanet.net.au/cfa/pager-cfa.php"
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        messages = soup.find_all("td")  # Adjust this selector based on actual HTML structure
        return [msg.text.strip() for msg in messages]
    return []

# Parse pager message based on your known structure
def parse_pager_message(message):
    pattern = r"@@ALERT (.*?) (.*?) (.*?) (.*?) \((\d{6})\) (.*?) (.*?) F(\d+)"
    match = re.search(pattern, message)

    if match:
        return {
            "Response Table Reference": match.group(1),
            "Incident Type & Response": match.group(2),
            "Incident Description": match.group(3),
            "Address": match.group(4),
            "Grid Reference": match.group(5),
            "Services Paged": match.group(6),
            "Appliances/Brigades Paged": match.group(7),
            "FIRS Number": match.group(8)
        }
    return None

# Send alert to the appropriate Discord channel
async def send_alert(guild_id, incident):
    conn = sqlite3.connect("data/bot_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT alert_channel, mention_role FROM settings WHERE guild_id=?", (guild_id,))
    settings = cursor.fetchone()
    conn.close()

    if settings:
        alert_channel_id, mention_role_id = settings
        channel = bot.get_channel(alert_channel_id)
        mention_role = f"<@&{mention_role_id}>" if mention_role_id else ""

        if channel:
            embed = discord.Embed(title="🚨 Emergency Alert 🚨", color=0xff0000)
            embed.add_field(name="Incident Type", value=incident["Incident Type & Response"], inline=False)
            embed.add_field(name="Description", value=incident["Incident Description"], inline=False)
            embed.add_field(name="Address", value=incident["Address"], inline=False)
            embed.add_field(name="Services Paged", value=incident["Services Paged"], inline=False)
            embed.add_field(name="Appliances/Brigades", value=incident["Appliances/Brigades Paged"], inline=False)
            embed.add_field(name="FIRS Number", value=incident["FIRS Number"], inline=False)

            await channel.send(content=mention_role, embed=embed)

# Command to add a Capcode to watch
@bot.tree.command(name="addcapcode", description="Add a Capcode to monitor")
async def add_capcode(interaction: discord.Interaction, capcode: str):
    guild_id = interaction.guild.id
    conn = sqlite3.connect("data/bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO capcodes (guild_id, capcode) VALUES (?, ?)", (guild_id, capcode))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ Capcode `{capcode}` added for this server!", ephemeral=True)

# Command to set alert channel
@bot.tree.command(name="setalertchannel", description="Set the alert channel for Capcode notifications")
async def set_alert_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_id = interaction.guild.id
    conn = sqlite3.connect("data/bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (guild_id, alert_channel) VALUES (?, ?)", (guild_id, channel.id))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ Alerts will be sent to {channel.mention}", ephemeral=True)

# Command to set mentions (roles/users) for alerts
@bot.tree.command(name="setmentions", description="Set a role or user to be mentioned in alerts")
async def set_mentions(interaction: discord.Interaction, mention: discord.Role | discord.User):
    guild_id = interaction.guild.id
    conn = sqlite3.connect("data/bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (guild_id, mention_role) VALUES (?, ?)", (guild_id, mention.id))
    conn.commit()
    conn.close()
    await interaction.response.send_message(f"✅ Alerts will mention {mention.mention}", ephemeral=True)

# Monitor pager for new messages and check Capcodes
async def check_pager():
    while True:
        messages = fetch_latest_page()
        
        if messages:
            conn = sqlite3.connect("data/bot_data.db")
            cursor = conn.cursor()

            cursor.execute("SELECT guild_id, capcode FROM capcodes")
            capcode_data = cursor.fetchall()
            conn.close()

            for message in messages:
                parsed_incident = parse_pager_message(message)

                if parsed_incident:
                    for guild_id, capcode in capcode_data:
                        if capcode in message:
                            await send_alert(guild_id, parsed_incident)

        await asyncio.sleep(5)  # Check every 5 seconds

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    bot.loop.create_task(check_pager())

bot.run(TOKEN)
