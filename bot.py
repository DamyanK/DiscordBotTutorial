import discord, json
from discord.ext import commands

client = commands.Bot(command_prefix=">", case_insensitive=True)

@client.event
async def on_ready():
	print("Bot is ready!")

@client.command()
async def hello(cxt):
	await cxt.send("Hi!")

@client.command(aliases=["numbers"])
async def number(ctx,*,num):
	with open("numbers.json", "r") as json_file:
		numsData = json.loads(json_file.read())
		await ctx.send(numsData[num])

#Check with a member (без права)
@client.command(aliases=["c"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, num = 2):
	await ctx.channel.purge(limit = num)

@client.command(aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,*,reason = "No reason declared!"):
	#await member.send("..." + reason) --- DM
	await ctx.send(member.name + " has been kicked from this server for " + reason)
	await member.kick(reason=reason)

@client.command(aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,*,reason = "No reason declared!"):
	#await member.send("..." + reason) --- DM
	await ctx.send(member.name + " has been banned for " + reason)
	await member.ban(reason=reason)

client.run('token')
