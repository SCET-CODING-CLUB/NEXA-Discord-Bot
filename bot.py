import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from sys import argv
import json

# check command line argument 
if len(argv) == 1:
    _config = "test" 
elif len(argv) == 2:
    _config = argv[1]
else:
    print(F"Correct usage: python bot.py <config>\n{' '*29}default:\"test\"")
    raise SystemExit

# check if server-config.json exists
try:
    with open("server-config.json", "r") as f:
        config_data = json.load(f)
except FileNotFoundError:
    
    print("server-config.json file not found.\nCreating one...")

    with open("server-config.json", "w") as f:
        f.write(json.dumps({"test":{"GUILD_ID":0,"WELCOME_CHANNEL_ID":0,"CONTACT_PERSONEL":0}}, indent=4))

    print()
    print("Replace the 0s with actual id(s) in server-conig.json")
    print("Usage:\n\tpython bot.py <config>\n\t              default: \"test\"")
    print("Add more configs if neccessary")
    raise SystemExit

# check type of data
if not isinstance(config_data, dict):
    raise TypeError("server-config.json is in wrong format")

# extract config info
config = config_data.get(_config)
if config is None:
    raise LookupError(F"\"{_config}\" not present in server-config.json")

# load env variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = discord.Object(id=config["GUILD_ID"])
WELCOME_CHANNEL_ID = config["WELCOME_CHANNEL_ID"]
CONTACT_PERSONEL = config["CONTACT_PERSONEL"]

intents = discord.Intents.default()
intents.members = True  # Required for on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    try:
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(F"Server started on guild ID: {GUILD_ID}")
        print(f"🔁 Synced {len(synced)} application commands.")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# Slash Commands

@bot.tree.command(name="purpose", description="Know the purpose of Nexus Coding Club", guild=GUILD_ID)
async def purpose(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🎯 The purpose of Nexus Coding Club is to teach, learn, and grow together. "
        "We’re here to uplift each other through collaboration and peer learning."
    )

@bot.tree.command(name="daily", description="Learn about our daily activities", guild=GUILD_ID)
async def daily(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📅 Daily Activities at Nexus:\n"
        "We hold coding sessions every day at 2:15 PM in the Nexus Coding Club Office near the MBA IT Lab.\n\n"
        "Activities include:\n"
        "• Problem-solving\n"
        "• Code reviews\n"
        "• Peer programming\n"
        "• Technical discussions"
    )

@bot.tree.command(name="events", description="View our recent events", guild=GUILD_ID)
async def events(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🎉 Major Events Organized by Nexus Coding Club:\n"
        "• SparkQuest 2025 – 27-28 February 2025\n"
        "• ExpoGen 1.0 – 6th May 2025\n\n"
        "More exciting events are coming soon — stay tuned!"
    )


@bot.tree.command(name="roles", description="Understand the Nexus team structure", guild=GUILD_ID)
async def roles(interaction: discord.Interaction):
    with open("teamstruct.json", encoding="utf-8") as f:
        data = json.load(f)
     
    await interaction.response.send_message(
     "\n".join( data )
    )


@bot.tree.command(name="help", description="List of commands and contact", guild=GUILD_ID)
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🤖 NEXA Bot Command Guide:\n"
        "/purpose – Know why Nexus exists\n"
        "/daily – View our daily coding routine\n"
        "/events – Explore Nexus events\n"
        "/roles – See the team structure\n"
        "/about – About the Nexus Coding Club\n\n"
        F"📩 Need help? Contact <@{CONTACT_PERSONEL}>.",
        allowed_mentions=discord.AllowedMentions(users=False)
    )

@bot.tree.command(name="about", description="About Nexus Coding Club", guild=GUILD_ID)
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        "ℹ️ Nexus Coding Club is a student-driven tech community at SCET, focused on building coding skills, launching real-world projects and collaborating with peers. "
        "You can customize this message to fit your club's intro."
    )

# Welcome new members (in a public channel + send DM)
@bot.event
async def on_member_join(member):
    # Public welcome message
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"👋 Welcome to Nexus Coding Club, {member.mention}!\nUse `/help` to get started!"
        )

    # DM welcome message
    try:
        await member.send(
             "👋 **Welcome to the NEXUS Coding Club Discord Server!**\n\n"
        "You've just taken your first step into a vibrant community of tech enthusiasts, learners and innovators at SCET.\n\n"
        "**Here's what you can look forward to:**\n"
        "💻 Daily coding sessions at 2:15 PM in the Nexus Office (near MBA IT Office)\n"
        "🤝 Peer to peer programming, group problem-solving and project collaboration\n"
        "🚀 Real-world app development and skill-building workshops\n"
        "🎙️ Tech bootcamps, events, competitions and hackathons\n\n"
        "To get started, type `/help` in the server to see all available commands.\n"
        "Want to know what events and workshops we've hosted? Try `/events` in the server to explore more! 🎉\n\n"
        "We're excited to have you on board  let's learn, build and grow together! ✨"
        )
    except discord.Forbidden:
        # print(f"❌ Could not send DM to {member.name}  they may have DMs disabled.") This Will be the meesage will come that they have not opened there dms
        pass #Does nothing  If dms are disabled 
bot.run(TOKEN)
