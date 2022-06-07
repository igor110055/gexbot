import discord
from discord.ext import commands
from discord.ext.commands import bot
import config

CBOE_UPDATE_MINUTES = 16

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(minutes=CBOE_UPDATE_MINUTES)  # task runs every 60 seconds
    async def update_options_data(self):
        channel = self.get_channel(1234567)  # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

TOKEN = config.bot_token

bot = commands.Bot(command_prefix="!")

@bot.command(pass_context=True)
async def test(ctx):
    await ctx.send("Current SPX Gamma", file=discord.File("img/SPX_gex_by_strike.png"))

bot.run(TOKEN)