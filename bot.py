
import asyncio
from datetime import datetime
import utils
from discord.ext import commands
import discord
import praw
from keep_alive import keep_alive
import random
import magic8ball
import requests
from pyfiglet import figlet_format
intents = discord.Intents.all()

rules = [
	":one: No NSFW Content",
	":two: No Cursing or Bob will come to your House",
	":three: No Trolling",
	":four: No Asking for mod or admin - do the form.",
	":five: No Spam",
	":six: Respect others",
	":seven: No NSFW Nicknames, PfPs, etc.",
	":eight: Respect Discord's TOS and Guidelines(\n:link: <https://discord.com/terms>\n:link: <https://discord.com/guidelines>",
	":nine: No Bot abusing"
]


def get_prefix(bot,message):
	with open("prefix.json") as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]




client = commands.Bot(command_prefix="n$",case_insensitive=True,intents=intents)#get_prefix)
client.remove_command("help")

@client.command()
@commands.has_permissions(manage_guild=True)
async def dump_db(ctx,tname):
	cur = db.cursor()
	cur.execute(f"DROP TABLE IF EXISTS {tname}")
	db.commit()
	await ctx.message.add_reaction("👌")

@client.event
async def on_guild_join(guild):
	await guild.create_role(name="Muted (By @Norx)")
	print("MUTED Role Created")

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx,member:discord.Member):
	role = discord.utils.get(ctx.guild.roles, name="Muted (By @Norx)")
	await member.add_roles(role)
	await ctx.send(embed=discord.Embed(title=f':white_check_mark: {member} was Muted!',color=discord.Color.green()))
	


@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member:discord.Member):
	role = discord.utils.get(ctx.guild.roles, name="Muted (By @Norx)")
	await member.remove_roles(role)
	await ctx.send(embed=discord.Embed(title=f':white_check_mark: {member} was Muted!',color=discord.Color.green()))
	

@client.command(aliases=["emfy"])
async def emojify(ctx,*,text):
	final_string = ""
	for char in text:
		if char == " ":
			final_string += "\t"
		else:
			final_string += f':regional_indicator_{char.lower()}:'
	await ctx.send(final_string)

@client.command(aliases=["presence"])
async def status(ctx,member:discord.Member=None):
	if not member: member = ctx.author
	embed = discord.Embed(color=member.color, timestamp=datetime.utcnow())
	embed.set_author(name=member.name,icon_url=member.avatar_url)
	embed.add_field(name="Status",value=member.status,inline=False)
	embed.add_field(name="Activity",value=member.activity,inline=False)
	await ctx.send(embed=embed)

@client.command()
async def help(ctx):
	em = discord.Embed(color=discord.Color.blue())
	em.add_field(name="Help",value="Here are all currently working commands;",inline=False)
	em.add_field(name="n$ping",value="This command returns the ping")
	em.add_field(name="n$8ball <your question>",value="Ask the almighty 8 ball a Question")
	em.add_field(name="n$joke",value="Get a fresh joke")
	em.add_field(name="n$flip",value="Toss a coin")
	em.add_field(name="n$rule <rule Number>",value="Read the rules.")
	em.add_field(name="n$meme",value="A funny, fresh meme")
	em.add_field(name="n$whois <member>",value="See User Information")
	em.add_field(name="n$clear <amount>",value="Delete Messages")
	em.add_field(name="n$kick <@member> <reason>",value="Yeet a Member out of the Server")
	em.add_field(name="n$ban <@member> <reason>",value="Ban a Member")
	em.add_field(name="n$unban <member#0000>",value="Unban a Member")
	
	await ctx.reply(embed=em)

@client.command()
async def meme(ctx,subred="memes"):
	subred = subred.replace("r/","")
	msg = await ctx.send("Loading meme...")

	reddit = praw.Reddit(
		client_secret="secret",
		client_id="id",
		username="username",
		password="password",
		user_agent = 'norx'
	) 

	subreddit = reddit.subreddit(subred)
	all_subs = []
	top = subreddit.top(limit=350)

	for submission in top:
		all_subs.append(submission)

	random_sub = random.choice(all_subs)
	embed = discord.Embed(title=f"__{random_sub.title}__")
	embed.set_image(url=random_sub.url)
	embed.set_author(name=random_sub.author.name,icon_url=random_sub.author.icon_img)
	await msg.edit(content=f"<https://reddit.com/r/{subred}/> :white_check_mark:",embed=embed)

@client.command()
async def joke(ctx):
	json_like = await fetch("joke",ctx)
	await ctx.reply(json_like["joke"])

@client.command(name="8ball")
async def _8ball(ctx,*,question):
	await ctx.reply(random.choice(magic8ball.list))

@client.command(help="See the Bots latency")
async def ping(ctx):
	await ctx.reply(f"Pong! Does anyone even use this? {round(client.latency*1000)}ms")

@client.command()
async def chat(ctx,*,message):
	json_like = await fetch("chat",ctx)

@client.event
async def on_ready():
	while 1:
		for guild in client.guilds:
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"Over {guild.name}"))
			await asyncio.sleep(3)


@client.command(help="Make the Bot repeat what you said")
async def say(ctx,*,message:str):
	if "@" in message:
		return await ctx.send("Cannot mention other People in `say` Command")
	await ctx.message.delete()
	await ctx.send(message)

@client.command(help="Flip A Coin")
async def flip(ctx):
	await ctx.send(random.choice(["Heads :coin:","Tails :coin:"]))

@client.command()
async def rule(ctx,index:int=1):
	await ctx.send(rules[index-1])

@client.command()
async def clyde(ctx,*,message="Hello. I'm Clyde"):
	utils.writeClyde(message)

	await ctx.send(file=discord.File("msg.png"))

@client.command()
async def ascii(ctx,*,text):
	await ctx.message.delete()
	await ctx.send("```"+figlet_format(text, font='starwars')+"```")

@client.command(aliases=["bin"])
async def binary(ctx,text:int):
	await ctx.send(utils.textToBin(text))

@client.command()
async def whois(ctx,member:discord.Member=None):
	if not member:
		member = ctx.author

	em = discord.Embed(title=f"User Information for {member}",color=member.color)
	em.add_field(name="ID",value=member.id)
	em.set_thumbnail(url=member.avatar.url)
	em.set_footer(text=f"Requested by {ctx.author.display_name}",icon_url=ctx.author.avatar_url)
	await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx,pre="n!"):	
	with open("prefix.json") as f:
		prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = pre

	with open("prefix.json","w+") as f:
		json.dump(prefixes,f)

	await ctx.send(f"Prefix was changed to `{pre}`")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"Over Electro's Gang | {pre}help"))



@client.command()
@commands.has_permissions(manage_guild=True)
async def setup_db(ctx):
	embed = discord.Embed(title="Setting up the Database...")
	msg = await ctx.send(embed=embed)
	embed.add_field(name="Processing:",value="Loading `main.db`...",inline=False)
	await msg.edit(embed=embed)
	embed.add_field(name="Processing:",value="Dropping old Table `levels`",inline=False)
	await msg.edit(embed=embed)
	embed.add_field(name="Processing:",value="Writing new Table...",inline=False)
	await msg.edit(embed=embed)
	embed.add_field(name="Processing:",value="Saving changes...",inline=False)
	await msg.edit(embed=embed)
	embed.add_field(name="Processing:",value="Applying changes to database...",inline=False)
	await msg.edit(embed=embed)

@client.command(aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=1):
	await ctx.channel.purge(limit=amount+1)


@client.command(aliases=["yeet"])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member:discord.Member,*,reason="Unspecified"):
	try:
		await member.kick(reason=reason)
		await ctx.send(embed=discord.Embed(title=f':white_check_mark: {member} was kicked!',color=discord.Color.green()))
	except Exception as ex:
		await ctx.send(embed=discord.Embed(title=f':x: {ex} ',color=discord.Color.red()))
		

@client.command(aliases=["permayeet"])
@commands.has_permissions(ban_members=True)
async def ban(ctx,member:discord.Member,*,reason="Unspecified"):
	try:
		await member.ban(reason=reason)
		await ctx.send(embed=discord.Embed(title=f':white_check_mark: {member} was banned!',color=discord.Color.green()))
	except Exception as ex:
		await ctx.send(embed=discord.Embed(title=f':x: {ex} ',color=discord.Color.red()))

@client.command(aliases=["unyeet"])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	mname, mdisc = member.split("#")

	for b in banned_users:
		user = b.user

		if(user.name, user.discriminator)==(mname,mdisc):
			await ctx.guild.unban(user)
			return await ctx.send(embed=discord.Embed(title=f':white_check_mark: {member} was Unbanned!',color=discord.Color.green()))

	await ctx.send(f"{member} wan't found!")
client.run("TOKEN")

