import os

import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message): 
    if message.author == bot.user:
        return
    
    if any(phrase.lower() in message.content.lower() for phrase in codephrases):
        print(message.content + " seen hamster mode activated!")
        try:
            await message.channel.send(
                content=message.author.mention + " " + get_death_message(),
                reference=message
            )
        except Exception as e:
            print(e)
            await message.channel.send("oops I fucked up...")

    await bot.process_commands(message)  # IMPORTANT

def load_codephrases():
    try:
        with open("codephrases.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def get_death_message():
    try:
        with open("death_messages.txt", "r", encoding="utf-8") as f:
            deatharr = [line.strip() + " " for line in f if line.strip()]
            return random.choice(deatharr) if deatharr else "You died happily on a farm "
    except FileNotFoundError:
        return "I cant seem to find how you died..."

def main():
    global codephrases
    codephrases = load_codephrases()
    try:
        with open('token.txt','r') as tkn:
            token = tkn.readline().strip()
    except:
        print("input token:")
        token = input()
        with open('token.txt','wt') as tkn:
            tkn.write(token) 
    bot.run(token)
    
    
main()