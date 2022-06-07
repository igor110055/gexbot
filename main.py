import time
import pandas as pd

from api.scrape_data import scrape_data

from calcs.compute_gex import compute_total_gex
from calcs.gex_by_strike import compute_gex_by_strike

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import discord
import os

TOKEN = os.environ.get("DISCORD_TOKEN")
fsociety_channel_id = os.environ.get("FSOCIETY_LIVEGEX_ID")

channel_ids = {
    "fsociety_livegex_id" : fsociety_channel_id
}
bot = discord.Client()

def draw_graphs(spot, option_data, timestamp):
    gex_oi, gex_volume = compute_total_gex(spot, option_data)
    compute_gex_by_strike(ticker, spot, option_data, gex_oi, gex_volume, timestamp)

async def emit_gamma():
    await bot.wait_until_ready()
    fsociety_channel = bot.get_channel(channel_ids["fsociety_livegex_id"])
    with open('SPX_gex_by_strike.png', 'rb') as f:
        picture = discord.File(f)
        await fsociety_channel.send(file=picture)
    with open('SPY_gex_by_strike.png', 'rb') as f:
        picture = discord.File(f)
        await fsociety_channel.send(file=picture)

scheduler = BlockingScheduler()
scheduler.add_job(draw_graphs, CronTrigger(day_of_week="mon-fri", minute="1"))
scheduler.add_job(emit_gamma, CronTrigger(day_of_week="mon-fri", minute="1"))

scheduler.start()

if __name__ == "__main__":

    bot.run(TOKEN)