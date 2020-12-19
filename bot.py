import discord, json
from discord.ext import commands

client = commands.Bot(command_prefix=">", case_insensitive=True)

#SIGNAL READY
@client.event
async def on_ready():
	print("Bot is ready!")

@client.command()
async def hello(cxt):
	await cxt.send("Hi!")

#Test if we can extract from a json file
@client.command(aliases=["numbers"])
async def number(ctx,*,num):
	with open("numbers.json", "r") as json_file:
		numsData = json.loads(json_file.read())
		await ctx.send(numsData[num])

#CLEAR TEXT
#Check with a member (без права)
@client.command(aliases=["c"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, num = 2):
	await ctx.channel.purge(limit = num)

#KICK
#Check too
@client.command(aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,*,reason = "No reason declared!"):
	#await member.send("..." + reason) --- DM
	await ctx.send(member.name + " has been kicked from this server for " + reason)
	await member.kick(reason=reason)

#BAN
@client.command(aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,*,reason = "No reason declared!"):
	#await member.send("..." + reason) --- DM
	await ctx.send(member.name + " has been banned for " + reason)
	await member.ban(reason=reason)

#UNBAN
@client.command(aliases=["ub"])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
	banned = ctx.guild.bans()
	name, tag = member.split("#")

	for i in banned:
		temp = i.user

		if temp.name == name and temp.discriminator == tag:
			await ctx.guild.unban(temp)
			await ctx.send(temp.name + " was unbanned!")
			return
	
	await ctx.send(member + " was not found!")

#MUTE
@client.command(aliases=["m", "mt"])
@commands.has_permissions(kick_members=True)
async def mute(ctx,member : discord.Member):
	# add id here
	muted = ctx.guild.get_role() # To get the id type \@RoleName
	await member.add_roles(muted)
	await ctx.send(member.mention + " has been muted!")

#UNMUTE
@client.command(aliases=["um", "umt"])
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member : discord.Member):
	# add id here
	muted = ctx.guild.get_role() # To get the id type \@RoleName
	await member.remove_roles(muted)
	await ctx.send(member.mention + " has been muted!")

# add token
client.run('')
