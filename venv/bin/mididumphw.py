#!/Users/Michael/PycharmProjects/MidiDiscordBot/venv/bin/python
"""
Print a description of the available devices.
"""
import midi.sequencer as sequencer

s = sequencer.SequencerHardware()

print(s)
