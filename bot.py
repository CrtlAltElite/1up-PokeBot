import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# https://discordpy.readthedocs.io/en/stable/api.html

# Create an app on the developer portal https://discord.com/developers/applications
    # Give it a name and agree to TOS.
    # Optional: Fill out App information.
    # Click "Bot" on the Left Menu.
        # Click "Reset Token".
        # Copy the Token and save this information; you will not be able to retrieve it later.
            # Be sure to keep this token private and DO NOT upload to GitHub (Discord will find it immediately and ban your bot).
        # On the Bot Page turn on Presence Intent, Server Members Intent, MESSAGE CONTENT INTENT
    # Set the app's Permissions:
        # Click on "OAuth2" on the left menu -> "URL Generator".
        # Click the box for "bot".
        # A new set of privileges should appear. Click the desired privileges (in our case: Send Messages, Add Reactions, Read Message History).
        # A URL is now in the "Generated URL" spot at the bottom of the page. This is the URL to allow you to invite your bot to Discord servers. Visit that link and add the bot to any servers for which you are the administrator.


# Set up Your Local environment
# Create a new Virtual Environment
    # python -m venv venv
# Activate the virtual environment
    # On Mac/Linux
    # source venv/bin/activate
    # On Windows
    # venv\Scripts\activate
# Install the tools we need
    # pip install requests python-dotenv discord
# Create a .env file
    # in the .env file add the line
    # DISCORD_BOT_TOKEN=YOUR_TOKEN_FROM_DISCORD_SITE
        # Note: No spaces around the equal sign
        # This is the token fromthe Bot page of the Discord site we retrieved earlier
# Create a gitignore (If you are uploading this project to github)
    # Add these two lines to your gitignore (and any others you feel you need)
    # venv/
    # .env


# Load the environmental variables (The Toke from Discord)
load_dotenv()
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')  # Replace 'DISCORD_BOT_TOKEN' with your bot's token in your .env

intents = discord.Intents.all()  # This gets all the available intents.

# Set up the command prefix for the bot. In this case, we're using '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Get all Pokemon names and store them in a set for efficient lookup
POKE_URL = "https://pokeapi.co/api/v2/pokemon/"
response = requests.get(POKE_URL + "?limit=10000")  # Assuming there are less than 10000 Pokémon
all_pokemon_names = {pokemon['name'] for pokemon in response.json()['results']}


@bot.event
async def on_ready():
    """Prep our app after connecting to the server"""

    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    
@bot.event
async def on_member_join(member):
    """Responds with a greeting to the user when they join"""
    await member.send(f'Welcome to the Unova server, {member.name}!')

@bot.command()
async def hello(ctx):
    """Responds with a greeting."""
    await ctx.send("Hello there from Unova!")

@bot.listen('on_message')
async def on_message(message):
    """Listens for mentions of pokemon names and replies with their image"""

    # Ensure the bot doesn't respond to its own messages
    if message.author == bot.user:
        return
    
    # To Copy and Paste the standard Emojis
    # Windows: Press Windows + . (period) or Windows + ; (semicolon) to open the emoji picker. Navigate to the desired emoji, click on it, and it will be inserted where your cursor is.
    # Mac: Press Command + Control + Space to open the emoji picker.
    # Linux: Depending on your distribution and desktop environment, there might be an emoji picker available. If not, you might have to copy and paste the emoji from an online source.
    # https://unicode.org/emoji/charts/full-emoji-list.html OR https://emojipedia.org/

    if "hello" in message.content.lower():
        await message.add_reaction("👋")

    # Check if it's a command message
    ctx = await bot.get_context(message)
    if ctx.valid:  # This means the message is a command
        return # Don't process command messages

    # Split the message content into words and convert to lowercase for comparison
    words = {word.lower() for word in message.content.split()}

    # Find the intersection of the two sets
    matching_pokemon_names = words.intersection(all_pokemon_names)

    # If there's a match
    for pokemon_name in matching_pokemon_names:
        response = requests.get(POKE_URL + pokemon_name)
        if response.status_code == 200:
            data = response.json()
            sprite_url = data.get('sprites').get('versions').get('generation-v').get('black-white').get('animated').get('front_default')


            if not sprite_url:
                sprite_url = data['sprites']['front_default']

            # Send the sprite image as a response
            embed = discord.Embed(title=f"You mentioned {pokemon_name}!")
            embed.set_image(url=sprite_url)
            await message.channel.send(embed=embed)




bot.run(TOKEN)
