import discord
from discord.ext import commands
import asyncio

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if member joined a voice channel
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel
        try:
            # Join the voice channel
            voice_client = await voice_channel.connect()
        except discord.ClientException:
            # Already connected to a channel
            voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

        # Play the Skype ringtone sound
        if not voice_client.is_playing():
            audio_source = discord.FFmpegPCMAudio("skype_ringtone.mp3")
            voice_client.play(audio_source)

            # Wait until the audio is done playing
            while voice_client.is_playing():
                await asyncio.sleep(1)

            # Disconnect after playing
            await voice_client.disconnect()

bot.run(TOKEN)
