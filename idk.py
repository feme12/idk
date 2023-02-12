import discord
import requests

# Replace YOUR_DISCORD_BOT_TOKEN with your actual Discord bot token
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"

# Replace YOUR_ROBLOX_API_KEY with your actual Roblox API key
ROBLOX_API_KEY = "YOUR_ROBLOX_API_KEY"

# List of whitelisted Roblox user IDs
whitelist = []

# Function to retrieve a user's Roblox ID from their Discord username
def get_roblox_id(username):
    response = requests.get(f"https://api.roblox.com/users/search?username={username}", headers={
        "Authorization": f"Bearer {ROBLOX_API_KEY}"
    })
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["id"]
    return None

# Discord bot client
client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!whitelist"):
        # Split the command and the username
        parts = message.content.split(" ")
        if len(parts) != 2:
            await message.channel.send("Usage: !whitelist <username>")
            return

        username = parts[1]
        roblox_id = get_roblox_id(username)
        if roblox_id is not None:
            # Add the user to the whitelist
            whitelist.append(roblox_id)
            await message.channel.send(f"{username} has been whitelisted with ID {roblox_id}")
        else:
            await message.channel.send(f"Could not find a matching Roblox account for username: {username}")

client.run(DISCORD_BOT_TOKEN)
