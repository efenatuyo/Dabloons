import discord
from discord.ext import commands
from discord import option
import asyncio
from webserver import keep_alive
import os
keep_alive()
#######################################################  Functions
import random
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read('database.ini')
def add_dabloon(userid, amount):
  numo=config[userid]['dabloons']
  a = int(numo) + int(amount)
  config[userid]['dabloons'] = str(a)
  with open('database.ini', 'w') as configfile:
            config.write(configfile)
  return "1"

  
def redeem_codes(code, userid):
  if code in config['codes']: 
    amount=config['codes'][code]
    if code in config[userid]:
      return "2"    #  Code already used
    else:  
      if add_dabloon(userid, amount) == "1":
       config[userid][code] = None
       with open('database.ini', 'w') as configfile:
            config.write(configfile)
       return "3"    #  Succes
  else:
    return "1"    #  Code does not exists

def create_codes(name):
  codename=name
  if codename in config['codes']:
    return "1"    #  Code already created
  else:
    dabloons = random.randint(1, 100)
    config["codes"][codename] = str(dabloons)
    with open('database.ini', 'w') as configfile:
            config.write(configfile)
    return "2"    #  Succes

#######################################################  Functions
#######################################################  Discord Bot
bot = commands.Bot()

@bot.event
async def on_ready():
  print('bot online')

########################### Help command
@bot.slash_command()
@option("help", description="Choose with what you need help with", choices=["creating codes", "claiming codes", "balance", "Give dabloons", "shop"])
async def help(ctx, help: str):

  if help == "creating codes":
      embed=discord.Embed(title="Creating codes", description="To create your own dabloon code you just have to use the command **/create_code** after that you will receive your code with dabloons on it. You can only create 5 Total dabloon codes. (Your code has a random dabloon amount from **1-100**) ", color=15105570)
      embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
      await ctx.respond(embed=embed)
  if help == "claiming codes":
    embed=discord.Embed(title="Claiming codes", description="To claim a code you have to use the **/redeem_code** command. After that the amount of dabloons in the code will be given to you", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
  if help == "balance":
    embed=discord.Embed(title="Balance", description="To see the amount of **dabloons** you have just use the command **/balance** and your dabloons will be showen", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
  if help == "Give dabloons":
    embed=discord.Embed(title="Give dabloons", description="To give other people dabloons just use the **/give_dabloons** command", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
  if help == "shop":
    embed=discord.Embed(title="Shop", description="shop is **not avaible** in this moment and is still under development.", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
########################### Help command
########################### Create code command
    
@bot.slash_command()
@option("name", description="Enter the name you want your code to be")
async def create_code(ctx, name: str):
  if str(ctx.author.id) in config["userids"]:
    pass
  else:
    config["userids"][str(ctx.author.id)] = None
    config[str(ctx.author.id)] = {}
    config[str(ctx.author.id)]["dabloons"] = "0"
    config[str(ctx.author.id)]["codestocreate"] = "5"
    with open('database.ini', 'w') as configfile:
            config.write(configfile)
  if int(config[str(ctx.author.id)]["codestocreate"]) == 0:
    embed=discord.Embed(title="Sorry but,", description=f"Yout can't create any new codes anymore.", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    return await ctx.respond(embed=embed)
  if create_codes(name) == "2":
    dabloons_amount=config["codes"][name]
    tries_left=config[str(ctx.author.id)]["codestocreate"]
    embed=discord.Embed(title="Created your code", description=f"Your code **{name}** has been succesfully created which has **{dabloons_amount}** dabloons in it.\nYou have {int(tries_left) -1} left custom codes to create", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
  
    response = await ctx.send(f'{ctx.author.mention}, take a look into your dms :) (message will be deleted in 5 seconds)')
    await ctx.author.send(embed=embed)
    await asyncio.sleep(5)
    await response.delete()
    total = int(tries_left) - 1
    config[str(ctx.author.id)]["codestocreate"] = str(total)
    with open('database.ini', 'w') as configfile:
            config.write(configfile)
  else:
    embed=discord.Embed(title="Sorry, but", description="this code has been already claimed please try a other one", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
########################### Create code command
########################### Redeem code command
@bot.slash_command()
@option("code", description="Enter the code you want to redeem")
async def redeem_code(ctx, code: str):
  if str(ctx.author.id) in config["userids"]:
    pass
  else:
    config["userids"][str(ctx.author.id)] = None
    config[str(ctx.author.id)] = {}
    config[str(ctx.author.id)]["dabloons"] = "0"
    config[str(ctx.author.id)]["codestocreate"] = "5"
    with open('database.ini', 'w') as configfile:
            config.write(configfile)
  if redeem_codes(code, str(ctx.author.id)) == "3":
      total = config["codes"][code]
      embed=discord.Embed(title="Yaay,", description=f"Succesfully added **{total}** dabloons to your balance.", color=15105570)
      embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
      await ctx.respond(embed=embed)
  else:
    
   if redeem_codes(code, str(ctx.author.id)) == "1":
    embed=discord.Embed(title="Sorry, but", description=f"your code **{code}** does not exists.", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    await ctx.respond(embed=embed)
   else:
     
    if redeem_codes(code, str(ctx.author.id)) == "2":
      embed=discord.Embed(title="Sorry, but", description=f"Sorry but you already used {code}.", color="#fcba03")
    
      embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
      await ctx.respond(embed=embed)
########################### Redeem code command
########################### Balance command
@bot.slash_command()
async def balance(ctx, user: discord.Option(discord.Member, required=False)):
  if user == None:
    if str(ctx.author.id) in config["userids"]:
     amount=config[str(ctx.author.id)]["dabloons"]
     embed=discord.Embed(title=f"{ctx.author.name} balance,", description=f"{ctx.author.mention} has {amount} dabloons in the bank", color=15105570)
     embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
     await ctx.respond(embed=embed)
  else:
    if str(user.id) in config["userids"]:
      amount=config[str(user.id)]["dabloons"]
      embed=discord.Embed(title=f"{user.name} balance,", description=f"{user.mention} has {amount} dabloons in the bank", color=15105570)
      embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
      await ctx.respond(embed=embed)
########## Balance command 
########## Give dabloons command
@bot.slash_command(guild_ids=[1046751276039405598])
@option("amount", description="Enter the amount you want to give")
async def give_dabloons (ctx, user: discord.Option(discord.Member, required=True), amount: str): 
  if ctx.author.id == user.id:
    embed=discord.Embed(title=f"Sorry but,", description=f"You can't give **yourself** dabloons", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    return await ctx.respond(embed=embed)
  if str(user.id) not in config["userids"]:
    embed=discord.Embed(title=f"Sorry but,", description=f"This user never used this bot before means that you are not able to give the person dabloons", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    return await ctx.respond(embed=embed)
  if int(amount) > int(config[str(ctx.author.id)]["dabloons"]):
    embed=discord.Embed(title=f"Sorry but,", description=f"You can't give more dabloons than you have", color=15105570)
    embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
    return await ctx.respond()
  giveramount = config[str(ctx.author.id)]["dabloons"]
  receiveramount = config[str(user.id)]["dabloons"]
  config[str(ctx.author.id)]["dabloons"] = str(int(giveramount) - int(amount))
  config[str(user.id)]["dabloons"] = str(int(receiveramount) + int(amount))
  with open('database.ini', 'w') as configfile:
            config.write(configfile)
  embed=discord.Embed(title=f"Yaay,", description=f"{user.mention} has received **{amount}** dabloons.", color=15105570)
  embed.set_thumbnail(url="https://d1fdloi71mui9q.cloudfront.net/LveXjedrSAiHfDC50OyQ_IMG_1555.PNG")
  await ctx.respond(embed=embed)
     
  
########## Give dabloons command    
bot.run('')
#######################################################  Discord Bot
    
    
     
