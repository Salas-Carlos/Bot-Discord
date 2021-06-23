import discord
from discord import channel
from discord import guild
from discord.client import Client
from discord.colour import Color
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import datetime
import schedule
from apscheduler.triggers.cron import CronTrigger

import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from urllib import parse, request
import re
#custom library
from Music import music
from Jobs import Meet

cliente = Client()
scheduler = AsyncIOScheduler()
bot = commands.Bot(command_prefix='!')


#--------------------------COMANDOS DE MUSICA---------------------------------------
@bot.command()
async def join(ctx, *, search):
   
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    Music = music(search)
    file  = Music.Descargar()
    await ctx.send(Music.url)
    source = FFmpegPCMAudio(executable="C:/Music/ffmpeg.exe", source=file)
    player = voice.play(source)

@bot.command()
async def YT(ctx, *, search):    
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('\"url\":\"/watch\\?v=(.{11})', html_content.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

@bot.command()
async def fuera(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        ctx.send("")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_playing():
        voice.pause()

@bot.command()
async def resumen(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_paused():
        voice.resume()

#-----------------------------------------------------------------------------


#--------------------------COMANDOS DE Prueba---------------------------------------
@bot.command()
async def test(ctx):
    await ctx.send("Comando de prueba")
    

@bot.command()
async def info(ctx):    
    embed = discord.Embed(title=f"{ctx.guild.name}", description="lorim impsum", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="server owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="server region", value=f"{ctx.guild.region}")
    embed.add_field(name="server ID", value=f"{ctx.guild.id}")
    #embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg")
    await ctx.send(embed=embed)

#------------------------------------------------------------------------------------

#--------------------------COMANDOS DE TAREAS PROGRAMADAS---------------------------------------
@bot.command()
async def meeting(ctx, * , informationGeneral):
    information = informationGeneral.split(sep=', ')
    if(len(information)==4):
        try: 
            date = datetime.datetime.strptime(information[2], '%Y-%m-%d %H:%M')
            job = Meet(information)
            job.save()
            await ctx.send("Reunion guardada")
        except ValueError:
            await ctx.send("La fecha no es valida")
    else:
        await ctx.send('Se debe enviar de esta manera "Titulo", "Descripcion", "fecha", "integrantes"')

 #-------------------------------------------------------------------------------------------



def jobs():
    job = Meet().addJobs(scheduler,bot)
   
@bot.event
async def on_ready():
    scheduler.add_job(jobs, 'interval', seconds = 5)
    print('My Bot is Ready')
    scheduler.start()
    

bot.run('ODUwOTI2MzQ3MzgzNDcyMTU4.YLw06g.LOZoOoQZFBPzq1kjkG69p8exOU0')



