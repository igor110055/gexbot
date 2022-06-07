import time
import pandas as pd

from api.scrape_data import scrape_data

from calcs.compute_gex import compute_total_gex
from calcs.gex_by_strike import compute_gex_by_strike


import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

CBOE_UPDATE_MINUTES = 16




def draw_graphs(spot, option_data, timestamp):
    gex_oi, gex_volume = compute_total_gex(spot, option_data)
    compute_gex_by_strike(ticker, spot, option_data, gex_oi, gex_volume, timestamp)


if __name__ == "__main__":
    # ticker = '_SPX'
    # # ticker = 'SPY'
    # spot, option_data, timestamp = scrape_data(ticker)
    
    # draw_graphs(spot, option_data, timestamp)
    bot.run(TOKEN)