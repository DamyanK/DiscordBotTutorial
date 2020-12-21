import discord, json, random
from discord.ext import commands

TOKEN = "Nzc4NDA2MDMyMzI1MjE0MjM4.X7RhHA.4J2HFae3wcJFCyrU0MRPicDBoK4"
client = commands.Bot(command_prefix=">", case_insensitive=True)

#SIGNAL READY
@client.event
async def on_ready():
	print("Bot is ready!")

#FILTER MESSAGES
@client.event
async def on_message(msg):
	filtered = [line.strip() for line in open("banned_words.txt", 'r')]

	for word in filtered:
		string = msg.content
		if word in string.lower():
			await msg.delete()

	await client.process_commands(msg)

#FIX ERRORS
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("You don't have the required permissions!")
		await ctx.message.delete()
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You missed to fill the whole argument!")
		await ctx.message.delete()
	else:
		raise error

@client.command()
async def hello(cxt):
	await cxt.send(random.choice(["Hi!", "Hello there!", "Hey!", "Nice to see you!"]))

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

#EMBED FOR INFO ABOUT USER
@client.command()
async def show(ctx, member : discord.Member):
	color = random.choice([discord.Colour.red(), discord.Colour.green(), discord.Colour.blue()])
	field = discord.Embed(title = member.name, description = member.mention,
	 color = color)
	field.add_field(name = "ID", value = member.id, inline = True)
	#field.add_field(name = "Role", value = member.top_role.name, inline = True)
	field.add_field(name = "Roles", value = [role.name for role in member.roles])
	field.set_thumbnail(url = member.avatar_url)
	field.set_footer(icon_url = ctx.author.avatar_url, text = f"- {ctx.author.name}")
	await ctx.send(embed = field)

# add token
client.run(TOKEN)