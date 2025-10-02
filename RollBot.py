import discord
from discord.ext import commands
import random
from enum import Enum
import json

'''
Bot made using the guidence of these sources
https://www.youtube.com/watch?v=CHbN_gB30Tw
https://www.youtube.com/watch?v=26Sj5hJFqUs
https://www.geeksforgeeks.org/python/read-json-file-using-python/
'''

''' Loading Token and GuildId from the secrets file '''
jsonData = {}

with open('RollBot Secrets.json', 'r') as file:
    jsonData = json.load(file)

TOKEN = jsonData.get('Token')
GUILD_ID = jsonData.get('GuildId')
GUILD_REFERENCE = discord.Object(id=GUILD_ID)

class rollConditions(Enum): 
    NONE = 1,
    ADVANTAGE = 2,
    DISADVANTAGE = 3

''' Starting the bot '''
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on to Discord as {self.user}')

        try:            #Syncing to the server
            guild = discord.Object(id=GUILD_ID)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands')

        except Exception as e:
            print(f'error: {e}')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

''' Slash Commands '''

'''Rolls the given number of dice with the given number of sides. Can be with advantage or disadvantage'''
@client.tree.command(name="roll", description="Roll dice with X sides, with the ability to automatically roll advantage or disadvantage", guild=GUILD_REFERENCE)
async def Rolldice(interaction:discord.Interaction, number_of_sides: int, number_of_dice: int = 1, condition: rollConditions = rollConditions.NONE):
    results: str = ''

    for i in range(number_of_dice):
        result = Roll(number_of_sides, condition) 
        results += f'\n{result}'

    await interaction.response.send_message(f"you rolled a: {results}")

''' "regular" commands '''

'''Clears "ammount" number of chats or the whole channel feed if not specified
**ONLY USE THIS WITH PEOPLE YOU TRUST, ANYONE CAN USE IT**
'''
@client.command()
async def clear(ctx, ammount: int = -1):
    if(ammount == -1):
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit = ammount)

''' Helper methods '''
#returns a random number between 1 and the number of sides of the die
def DiceRoll(sides: int):
    return random.randint(1, sides)


def Roll(sides: int, condition: rollConditions):      
    if(condition == rollConditions.NONE):                                               #rolls 1 die if there is no advantage/disadvantage
        return str(DiceRoll(sides))
                
    #I think you only roll d20s with advantage/disadvantage but I'm not 100% sure so I left the option to roll others
    results = []
    for i in range(2):                                                                  #rolling 2 dice
        results.append(DiceRoll(sides))

    result = max(results) if condition == rollConditions.ADVANTAGE else min(results)    #choosing the higher/lower roll
    return f'{result}, ({results[0]}, {results[1]})'

client.run(TOKEN)