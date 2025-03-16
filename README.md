**# Emergency Pager Discord Bot

## Description
This bot monitors a Victorian Emergency Service pager website and alerts users based on specified Capcodes.

## Setup

1. **Clone the repository**:
git clone https://github.com/SamJustSam-create/VicFires.git

2. **Install dependencies**:
pip install discord.py beautifulsoup4 requests

3. **Set up your config file**:
- Create `config/config.json` and insert your bot token:
```json
{
    "TOKEN": "YOUR_DISCORD_BOT_TOKEN"
}

4. **Run the bot**:
python3 bot.py

5. **Commands**:
/addcapcode <capcode> - Add a Capcode to monitor.
/setalertchannel <#channel> - Set the alert channel for this server.
/setmentions @role - Set a role/user to mention when an alert occurs.

---

### **7. Optional Modularization**

If your bot grows, you can split functionality into cogs (modularized components). For example, the Capcode management can be in a separate cog (`capcodes.py`).

**Example `cogs/capcodes.py`:**

```python
from discord.ext import commands
import sqlite3

class Capcodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addcapcode(self, ctx, capcode: str):
        guild_id = ctx.guild.id
        conn = sqlite3.connect("data/bot_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO capcodes (guild_id, capcode) VALUES (?, ?)", (guild_id, capcode))
        conn.commit()
        conn.close()
        await ctx.send(f"✅ Capcode `{capcode}` added for this server!")

def setup(bot):
    bot.add_cog(Capcodes(bot))

Then, load it in the main bot file:

@bot.event
async def on_ready():
    bot.load_extension('cogs.capcodes')
**Certainly! Here's a detailed `README.md` file for your Discord bot project:

```markdown
# Emergency Pager Discord Bot

## Overview
This Discord bot monitors a Victorian Emergency Service pager website and sends real-time notifications to Discord channels based on specific Capcodes. When an incident page containing a monitored Capcode is detected, the bot parses the page data and sends an embedded message with the incident details to the configured Discord channels.

## Features
- **Capcode Monitoring**: Track specific Capcodes and get alerted when a page is detected for them.
- **Real-Time Updates**: Continuously monitor the Victorian Emergency Service pager website for new incidents.
- **Customizable Alerts**: Set custom alert channels and role/user mentions for each Discord server.
- **Modular and Scalable**: Easily add additional features and expand the bot with new functionalities as needed.

## Requirements
Before running the bot, ensure you have the following:
- **Python 3.8+** installed on your machine
- **Discord Bot Token** (obtainable from the [Discord Developer Portal](https://discord.com/developers/applications))

### Dependencies
You will need to install the following Python packages:
- `discord.py` - The official Python library for Discord API interactions.
- `beautifulsoup4` - A library for scraping HTML content from the pager website.
- `requests` - For making HTTP requests to the pager website.

Install these dependencies by running:
```bash
pip install discord.py beautifulsoup4 requests
```

## Setup Instructions

### 1. Clone the Repository
Clone the bot's repository to your local machine:
```bash
git clone https://github.com/yourusername/emergency-pager-bot.git
cd emergency-pager-bot
```

### 2. Configure Your Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application (if you don't already have one).
3. Navigate to the **Bot** section and copy your bot token.

Create a `config/config.json` file in your project directory and paste the following content:
```json
{
    "TOKEN": "YOUR_DISCORD_BOT_TOKEN"
}
```
Replace `"YOUR_DISCORD_BOT_TOKEN"` with the token you copied earlier.

### 3. Create the Database
The bot uses an SQLite database to store Capcodes and server settings (such as alert channels and mentions). The database will be automatically created the first time you run the bot, so you don't need to worry about this step.

### 4. Run the Bot
To start the bot, simply run:
```bash
python3 bot.py
```

### 5. Bot Commands
Once the bot is running, you can use the following Discord slash commands to interact with it:

#### `/addcapcode <capcode>`
Adds a Capcode to monitor. Replace `<capcode>` with the 4-character code you wish to track.
Example:
```
/addcapcode A123
```

#### `/setalertchannel <#channel>`
Sets the channel where alerts will be sent. Replace `<#channel>` with the desired text channel.
Example:
```
/setalertchannel #alerts
```

#### `/setmentions <@role|@user>`
Sets a role or user to be mentioned when an alert occurs. Replace `<@role|@user>` with the desired role or user.
Example:
```
/setmentions @firefighters
```

### 6. Bot Operation
- **Fetching Pager Messages**: The bot fetches new pager messages from the [Victorian Emergency Service Pager](https://mazzanet.net.au/cfa/pager-cfa.php) website every few seconds.
- **Alert Notification**: When a pager message is detected for a Capcode the bot is tracking, it parses the message and sends a detailed alert to the configured Discord channel with an embedded message that includes:
  - Incident Type
  - Incident Description
  - Address
  - Services Paged
  - Appliances/Brigades Paged
  - FIRS Number

## File Structure

The bot is structured as follows:

```
/discord-bot
│
├── /data                # Database and storage files
│   └── bot_data.db      # SQLite database for settings and capcodes
│
├── /bot                 # Bot logic and commands
│   ├── bot.py           # Main bot code
│   └── /cogs            # Optional: For modularizing commands
│       └── capcodes.py  # Capcode management logic
│
├── /config              # Config files for sensitive data (e.g., tokens)
│   └── config.json      # Store bot token and config here (or environment vars)
│
├── /logs                # Logs, if you decide to add them later
│   └── bot.log          # Log file
│
└── README.md            # Project overview and instructions
```

## Troubleshooting

### Common Issues:
1. **Bot Not Responding to Commands**:
   - Ensure the bot is running and connected to the Discord server.
   - Make sure the bot has the appropriate permissions to send messages and manage channels in the server.
   - Double-check the token in `config/config.json`.

2. **Database Issues**:
   - The bot automatically creates the `bot_data.db` SQLite database on the first run. If the database isn't created, ensure that your Python environment has write permissions in the project directory.

3. **Pager Website Not Updating**:
   - If the bot is not detecting new pages from the website, ensure that the webpage is accessible and that the bot is correctly scraping the content. You can test the web scraping functionality by running the `fetch_latest_page()` function outside the bot.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. If you encounter bugs or have suggestions for improvements, create an issue in the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **discord.py**: The official Python wrapper for the Discord API.
- **BeautifulSoup4**: A library for parsing HTML and XML documents.
- **Requests**: A simple HTTP library for making requests to external websites.
```

---

### **How to Customize the README**

- **Replace the `git clone` URL**: Make sure to replace `https://github.com/yourusername/emergency-pager-bot.git` with the actual URL of your repository.
- **Further Explanation**: Add more sections if you plan to add additional features in the future, like logging, error handling, or different ways of setting up Capcodes.

This `README.md` file provides a complete guide for setting up and running the bot, along with an overview of the project structure and functionality.
