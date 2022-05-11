from discord.ext import commands
from discord import Color
from discord.ext import tasks
from table2ascii import table2ascii as t2a, PresetStyle
import discord
import sqlite3
import json
import os
import time

blue = Color.blue()

#creates config file if it does not exist
if os.path.exists("config.json") == False:
    with open("config.json", "w") as json_file2:
        json_file2.write('{"token":"","prefix":""}')
        print("Config file created, please enter token and prefix into config.json and restart")
        exit()
else:
    #config loading if file exists
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

class Utility(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.DB = sqlite3.connect("qe.db")


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

        cursor = self.DB.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS subjects(user_id text,points integer,UNIQUE(user_id))")
        for guild in self.bot.guilds:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS report{guild.id}(id integer PRIMARY KEY, channel_id text)")
            self.DB.commit()
    


    @commands.Cog.listener()
    async def on_message(self,message):
        cursor = self.DB.cursor()
        crime_words = {'microwave','france','french','coffee','kill','murder','murdering','microwaving water','pat','stopsign','stop sign','magnamalo','khezu','alatreon'}
        if message.content in crime_words and message.author.id == 211542806680961024:
            cursor.execute('UPDATE purple_crimes SET keywords = keywords + 1 WHERE id = 1')
            self.DB.commit()


    @tasks.loop(seconds=60)
    async def purple_exectution(self):
        user = await self.bot.fetch_user(211542806680961024)
        channel = self.bot.get_channel(968669306453905458)
        cursor = self.DB.cursor()
        cursor.execute(f"Select pats,microwaves,keywords FROM purple_crimes ")
        crimes = cursor.fetchall()
        cursor.execute(f"Select points FROM subjects WHERE user_id = {211542806680961024}")
        credits = cursor.fetchone()
        if crimes[0][0] > 5 and crimes[1][0] > 5 and crimes[2][0] > 15 and credits < 500:


            embed=discord.Embed(title="Queen Elizabeth",description=f'{user.mention}',color=blue)
            embed.add_field(name=f"For your crimes directly against me you will be executed in 30 minutes!", value="Reflect on your actions before you are beheaded", inline=True)
            embed.set_image(url="https://cdn.discordapp.com/attachments/732902791735017503/968702601321381958/2.PNG")
            await channel.send(embed=embed)
            time.sleep(1800)
   
            embed=discord.Embed(title="Queen Elizabeth",description=f'{user.mention}',color=blue)
            embed.add_field(name=f"The time as come!", value="Let this be an example!", inline=True)
            embed.set_image(url="https://cdn.discordapp.com/attachments/732902791735017503/968702601321381958/2.PNG")
            await channel.send(embed=embed)
            time.sleep(5)
            await self.bot.kick(user)


    @commands.has_any_role("Book Keeper")
    @commands.command()
    async def set_report_channel(self,ctx): 
        cursor = self.DB.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO report{ctx.guild.id}(id,channel_id) VALUES(0,'{ctx.channel.id}')") 
        cursor.execute(f"UPDATE report{ctx.guild.id} SET channel_id = '{ctx.channel.id}'  WHERE id = '0'")
        self.DB.commit()
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"Ledger update channel set!", value="You'll see weekly ledger reports here!", inline=True)
        await ctx.send(embed=embed)
 
    @commands.has_any_role("Book Keeper")
    @commands.command()
    async def register(self,ctx,user: discord.User):
        cursor = self.DB.cursor()
        cursor.execute(f"INSERT OR IGNORE INTO subjects(user_id,points) VALUES('{user.id}',500)") 
        self.DB.commit()
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{user.display_name} is a new royal subject!", value="Serve me well!", inline=True)
        embed.set_image(url="https://media.discordapp.net/attachments/732902791735017503/968702601069756466/1.PNG")
        await ctx.send(embed=embed)

    @commands.has_any_role("Book Keeper")
    @commands.command()
    async def add(self,ctx,amount,user: discord.User):
        points = str(amount)  
        cursor = self.DB.cursor()
        cursor.execute(f"UPDATE subjects SET points = points + {points}  WHERE user_id = '{user.id}'")
        self.DB.commit()
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{amount} credits have been awarded to {user.display_name}!", value="You better be grateful!", inline=True)
        embed.set_image(url="https://media.discordapp.net/attachments/732902791735017503/968702601069756466/1.PNG")
        await ctx.send(embed=embed)
    

    @commands.has_any_role("Book Keeper")
    @commands.command()
    async def remove(self,ctx,amount,user: discord.User):
        points = str(amount)  
        cursor = self.DB.cursor()
        cursor.execute(f"UPDATE subjects SET points = points - {points}  WHERE user_id = '{user.id}'")
        self.DB.commit()
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{amount} credits have been deducted from {user.display_name}!", value="How despicable! To have brought shame to the great Elizabeth! You better remember this!", inline=True)
        embed.set_image(url="https://cdn.discordapp.com/attachments/732902791735017503/968702601321381958/2.PNG")
        await ctx.send(embed=embed)
    
    @commands.has_any_role("Book Keeper")
    @commands.command()
    async def reset(self,ctx,user: discord.User):
 
        cursor = self.DB.cursor()
        cursor.execute(f"UPDATE subjects SET points = 500  WHERE user_id = '{user.id}'")
        self.DB.commit()
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{user.display_name}'s credits have been reset!", value="Back to peasantry!", inline=True)
        embed.set_image(url="https://cdn.discordapp.com/attachments/732902791735017503/968702601321381958/2.PNG")
        await ctx.send(embed=embed)

    


    @commands.command()
    async def credits(self,ctx,user: discord.User): 
        cursor = self.DB.cursor()
        cursor.execute(f"Select points FROM subjects WHERE user_id = {user.id}")
        points = cursor.fetchone() 
        
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{user.display_name} Currently has {points[0]} Royal Credits!!", value="Humu! Keep worshiping me!", inline=True)
        await ctx.send(embed=embed)



    @commands.command()
    async def my_credits(self,ctx):  
        cursor = self.DB.cursor()
        cursor.execute(f"Select points FROM subjects WHERE user_id = {ctx.message.author.id}")
        points = cursor.fetchone() 
        
        embed=discord.Embed(title="Queen Elizabeth",color=blue)
        embed.add_field(name=f"{ctx.message.author.display_name} Currently has {points[0]} Royal Credits!!", value="Humu! Keep worshiping me!", inline=True)
        await ctx.send(embed=embed)
 
   
    @commands.command()
    async def ledger(self,ctx):
        guild = ctx.guild.id
        cursor = self.DB.cursor()
        cursor.execute(f"SELECT user_id,points FROM subjects ORDER BY points DESC")  
        list_items = cursor.fetchall()

        ledger = []

        for item in list_items:
            name = await self.bot.fetch_user(item[0])
            ledger.append([name.display_name,item[1]])

       
        output = t2a(
            header=["Name", "Royal Credits"],
            body=ledger,
            style=PresetStyle.thin_compact
        )

        await ctx.send(f"```\n{output}\n```")    


    @commands.command()
    async def response(self,ctx,type,content):
        cursor = self.DB.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS responses(id integer PRIMARY KEY, response text)")
        self.DB.commit()
        if type.lower() == "add":
            cursor.execute(f'INSERT OR IGNORE INTO responses(response) Values("{content}")')
            self.DB.commit()
            await ctx.send("New response added!")
        elif type.lower() == "remove":
            pass

    @commands.command()
    async def pat(self,ctx):
        cursor= self.DB.cursor()
        cursor.execute(f"SELECT response from responses ORDER BY RANDOM() LIMIT 1;")
        response = cursor.fetchone()
        user =  await self.bot.fetch_user(265753047215505410)
        if ctx.message.author.id != 265753047215505410:
            await ctx.send(f"H-Hey! You're not {user.display_name}! I'll have you beheaded for this!")
        elif ctx.message.author.id == 265753047215505410:
            await ctx.send(response[0].format(user.display_name))

    
    @commands.command()
    async def monsters(self,ctx):
        await ctx.send(" Captures:\n\
```Tobi-          50\n\
Mizu-          50\n\
Viper Tobi-    49\n\
Seregios-      40\n\
Black Diablos- 40\n\
Lagiacrus-     40\n\
Yian Garuga-   40\n\
Diablos-       30\n\
Paolumu-       30\n\
Night Pao-     25\n\
Barioth(EXT)-  25\n\
Legiana(EXT)-  25\n\
Nargacuga-     25\n\
Kulu-Ya-Ku-    20\n\
Silver Rath-   15\n\
Stygian Zino-  15\n\
Rajang (MHR)-(-1)\n\
Rajang (MHW)-(-20)\n\
Jyuratodus-  (-50)```\
\nSlays:\n\
```Namielle-       50\n\
Alatreon-       50\n\
Fatalis-        50\n\
Magnamalo(EXT)- 50\n\
Shara Ishvalda- 40\n\
Xeno Jiva-      40\n\
Almudron(EXT)-  35\n\
Safi Jiva-      35```")
        
    @commands.command()
    async def microwave(self,ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/732898874364002326/974052785064665188/qe_hot_water.mp4')

        





