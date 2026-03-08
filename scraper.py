import requests
from bs4 import BeautifulSoup
from PIL import Image
import discord
from discord.ext import commands
from discord import app_commands
import random

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="/",intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message:discord.message):
    if message.author == bot.user:
        return

    if message.content.startswith('/motm'):
        print(message.content)
        try:
            number = (message.content.removeprefix("/motm").strip())
            if(number == "random" or number == "rand" or number == "rng"):
                handle_motm()
                maxnum = open('resources/txt/motm.txt','r').readline()
                number = random.randint(1,int(maxnum))
                handle_motm(number)
            if(int(number)):
                handle_motm(number)
            else:
                handle_motm()
                number = open('resources/txt/motm.txt','r').readline()
            file = discord.File("resources/jpg/"+number+'.jpg')
            await message.channel.send(file=file, content="yapping about molecules link here too also number of the motm: " + number )
        except:
            await message.channel.send("oops I fucked up...")
        


def bot_motm(message:str):
    pass

def scrape_motm(number = -1):
    response = requests.get('https://pdb101.rcsb.org/motm/motm-image-download')
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table')
    if table:
        for row in table.find_all('tr'):
            exists = row.find_all('a')
            if exists:
                id = exists[1].text.strip()
                if (number == -1):
                        if id:
                            return(id +";"+ exists[2].text +";"+ exists[3].get('href')+";"+"https://pdb101.rcsb.org/motm/"+exists[1].text.strip())
                elif(id == number):
                    return(id +";"+ exists[2].text +";"+ exists[3].get('href')+";"+"https://pdb101.rcsb.org/motm/"+exists[1].text.strip())
    return "2"
                
def download_tif(motm):
    link = motm.split(";")[2]
    print("Downloading tif")
    response = requests.get(link, allow_redirects=True)
    open("resources/tif/"+motm.split(";")[0]+'.tif', 'wb').write(response.content)
    print("Downloaded tif")


def convert_tif(motm):
    number = motm.split(";")[0]
    print("Converting to JPG")
    image = Image.open("resources/tif/"+number+'.tif')
    image = image.convert("RGB")
    image.save("resources/jpg/"+number+'.jpg','JPEG')
    print("Converted to JPG")

def save_motm(motm):
    print("Saving last motm")
    open("resources/txt/"+motm.split(";")[0]+'.txt','wt').write(motm)
    print("Saved motm")

def handle_motm(number = -1):
    
    if number != -1 and number:
        print("using this as the number: " + number)
        motm = scrape_motm(number)
    else:
        print("using base motm")
        motm = scrape_motm()
        open('resources/txt/motm.txt','wt').write(motm.split(";")[0]) 
    if motm:
        print(motm)
        download_tif(motm)
        convert_tif(motm)
        save_motm(motm)

def main():
    try:
        token = open('token.txt','r').readline()
    except:
        print("input token:")
        token = input()
        open('token.txt','wt').write(token) 
    bot.run(token)
    
    
main()