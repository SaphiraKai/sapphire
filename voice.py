from os import path
from subprocess import call, Popen, PIPE

voice_dir = path.join(path.dirname(path.realpath(__file__)), 'voice')

if not path.isdir(voice_dir):
	raise FileNotFoundError(f"'{voice_dir}' does not exist")


def play(sound, block=False):
	sound_path = path.join(voice_dir, sound + '.ogg')

	if path.exists(sound_path):
		if block:
			call(['mpv', sound_path], stdout=PIPE, stderr=PIPE)

		else:
			Popen(['mpv', sound_path], stdout=PIPE, stderr=PIPE)

	else:
		raise FileNotFoundError(f"'{sound_path}' does not exist")

