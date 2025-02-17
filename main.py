import discord
from discord.ext import commands
import os
import sys

from myserver import server_on

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot Started!")

@bot.command()
async def restart(ctx):
    await ctx.send("Bot is restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
async def vincere(ctx):
    await ctx.send(f'Hello team {ctx.author.mention}!')

@bot.event
async def on_member_join(member):
    print(f'Welcome {member.mention} to Vincere!')
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        emoji = discord.utils.get(member.guild.emojis, name='pop')
        if emoji:
            await channel.send(f'{emoji} Welcome {member.mention} to Vincere!')

@bot.event
async def on_member_remove(member):
    print(f'Goodbye {member.name} from Vincere')
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        emoji = discord.utils.get(member.guild.emojis, name='blink')
        if emoji:
            await channel.send(f'{emoji} Goodbye {member.mention} from Vincere!')

@bot.command()
async def playmusic(ctx, *, song_name):
    activity = discord.Activity(type=discord.ActivityType.listening, name=song_name)
    await bot.change_presence(activity=activity)
    emoji = discord.utils.get(ctx.guild.emojis, name='milkbear')
    if emoji:
        await ctx.send(f'Listening to: {emoji} {song_name}')

allowed_channel_id = 1339808191952982028

@bot.command()
async def give_role_react(ctx):
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("This command can only be used in the specific channel.")
        return

    message = await ctx.send("React with :MercyShy: to get the role and remove it by unreacting!")

    custom_emoji_1 = discord.utils.get(ctx.guild.emojis, name='MercyShy')

    if custom_emoji_1:
        await message.add_reaction(custom_emoji_1)
    else:
        await ctx.send("Custom emoji not found.")

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != allowed_channel_id:
        return

    if user.bot:
        return

    role_name = "Member"
    custom_emoji_1 = discord.utils.get(reaction.message.guild.emojis, name='MercyShy')
    role = discord.utils.get(reaction.message.guild.roles, name=role_name)

    if reaction.emoji == custom_emoji_1 and role:
        await user.add_roles(role)
        await user.send(f"You have been given the {role_name} role!")

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != allowed_channel_id:
        return

    if user.bot:
        return

    role_name = "Member"
    custom_emoji_1 = discord.utils.get(reaction.message.guild.emojis, name='MercyShy')
    role = discord.utils.get(reaction.message.guild.roles, name=role_name)

    if reaction.emoji == custom_emoji_1 and role:
        await user.remove_roles(role)
        await user.send(f"You have been removed from the {role_name} role!")

server_on()

bot.run(os.getenv('TOKEN'))