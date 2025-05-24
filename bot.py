import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=int(os.getenv("GUILD_ID")))  # You must set this in your .env file
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))  # Add this to your .env too

intents = discord.Intents.default()
intents.members = True  # Required for on_member_join

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    try:
        synced = await bot.tree.sync(guild=GUILD_ID)
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
        "🎉 Major Events Organized by Nexus:\n"
        "• SparkQuest 2025\n"
        "• ExpoGen 1.0\n"
        "More events coming soon — stay tuned!"
    )

@bot.tree.command(name="roles", description="Understand the Nexus team structure", guild=GUILD_ID)
async def roles(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🧑‍💻 Nexus Coding Club Team Hierarchy:\n"
        "• 👑 President: Abdul Samad\n"
        "• 🤝 Vice President: Abdul Rafey\n"
        "• 🧠 Technical Lead: Mohiuddin\n"
        "• 📢 PR & Social Media Manager: Mohammad Habib Hussain Alkaf\n"
        "• 🎯 Event Coordinators: Ayaan\n"
        "• 👥 Core Team Members: IDk\n"
        "• 👨‍🎓 General Members: All participating students"
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
        "📩 Need help? Contact <790539589470912513>."
    )

@bot.tree.command(name="about", description="About Nexus Coding Club", guild=GUILD_ID)
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        "ℹ️ Nexus Coding Club is a student-driven tech community at SCET, focused on building coding skills, launching real-world projects, and collaborating with peers. "
        "You can customize this message to fit your club's intro."
    )

# Welcome new members (in a public channel)
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"👋 Welcome to Nexus Coding Club, {member.mention}!\nUse `/help` to get started!"
        )

bot.run(TOKEN)
