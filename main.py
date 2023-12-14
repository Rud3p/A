import nextcord
import random
import requests
from nextcord.ext import commands

TOKEN = "MTE2NzkyODc5MTQ0NDc1NDU5NA.G4Y4DE.OP_FxdHb6-A-nIYr7LZQNnaF-d-O50JsoidlN8"

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

# Define the image categories from waifu.pics.
sfw_categories = [
    "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug",
    "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile",
    "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill",
    "kick", "happy", "wink", "poke", "dance", "cringe"
]

nsfw_categories = ["waifu", "neko", "trap", "blowjob"]

# Function to get a random image URL from the waifu.pics API.
def get_random_image_url(category, sfw=True):
    if sfw:
        if category not in sfw_categories:
            return None
    else:
        if category not in nsfw_categories:
            return None

    base_url = "https://api.waifu.pics"
    endpoint = "sfw" if sfw else "nsfw"
    url = f"{base_url}/{endpoint}/{category}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("url")
    else:
        return None

# Bot command to send random images.
@bot.command()
async def random(ctx, category, num: int = 1, mode="sfw"):
    if num < 1:
        await ctx.send("Please specify a valid number of images (1 or more).")
        return

    image_category = category.lower()

    if mode.lower() == "nsfw":
        sfw = False
    else:
        sfw = True

    if image_category in sfw_categories or image_category in nsfw_categories:
        for _ in range(num):
            image_url = get_random_image_url(image_category, sfw=sfw)
            await ctx.send(image_url)
    else:
        await ctx.send("Invalid category. Use `.help` to see available categories.")
        return

# Help command.
@bot.command()
async def catg(ctx):
    sfw_category_list = ", ".join(sfw_categories)
    nsfw_category_list = ", ".join(nsfw_categories)
    help_message = f"SFW categories: {sfw_category_list}\nNSFW categories: {nsfw_category_list}"
    await ctx.send(help_message)

# Run the bot.
bot.run(TOKEN)
