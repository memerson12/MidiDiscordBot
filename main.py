import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
from html2image import Html2Image
from midi2audio import FluidSynth
from pretty_midi import PrettyMIDI
from pydub import AudioSegment
from visual_midi import Plotter, Preset

load_dotenv(dotenv_path="tokens.env")
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="-")
client = discord.Client()


@bot.command(name="toMp3")
async def toMp3(ctx: commands.Context):
    message = ctx.message
    if len(message.attachments) == 0:
        await ctx.send(content="Error: Please attach file in message.")
        return
    await ctx.send(content="Converting...")

    output_file = convert_midi_to_audio(message.attachments[0].url)
    if output_file is not None:
        await ctx.send(content="Here is the converted file:", file=output_file)
    else:
        await ctx.send(content="Error: Sorry the converted file size was over the 8MB limit.")


@bot.command(name="toImage")
async def toImage(ctx: commands.Context):
    message = ctx.message
    if len(message.attachments) == 0:
        await ctx.send(content="Error: Please attach file in message.")
        return
    await ctx.send(content="Converting...")

    output_file = convert_midi_to_image(message.attachments[0].url)
    if output_file is not None:
        await ctx.send(content="Here is the image:", file=output_file)
    else:
        await ctx.send(content="Error: Sorry the converted file size was over the 8MB limit.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found!")


def convert_midi_to_audio(url):
    fs = FluidSynth()
    file = requests.get(url)
    open('input.mid', 'wb').write(file.content)
    fs.midi_to_audio('/Users/Michael/PycharmProjects/MidiDiscordBot/input.mid', 'output.wav')
    sound = AudioSegment.from_wav('output.wav')
    sound.export('output.mp3', format="mp3")
    return discord.File(r'output.mp3') if os.path.getsize('output.mp3') <= 16000000 else None


def convert_midi_to_image(url):
    file = requests.get(url)
    open('input.mid', 'wb').write(file.content)
    pm = PrettyMIDI("input.mid")
    preset = Preset(plot_width=1000, plot_height=500)
    plotter = Plotter(preset=preset)
    plotter.save(pm, 'imageHtml.html')
    hti = Html2Image()
    hti.screenshot(html_file='imageHtml.html', save_as='image.png', size=(1000, 500))
    return discord.File(r'image.png') if os.path.getsize('image.png') <= 16000000 else None


bot.run(TOKEN)
