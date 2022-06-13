from os import path
from subprocess import call, Popen, PIPE

#? directory containing voice sound files
voice_dir = path.join(path.dirname(path.realpath(__file__)), 'voice')

if not path.isdir(voice_dir):
	raise FileNotFoundError(f"'{voice_dir}' does not exist")


#? play a voice sound using mpv
def play(sound, block=False):
	sound_path = path.join(voice_dir, sound + '.ogg')

	if path.exists(sound_path):
		#? block until playing is complete
		if block:
			call(['mpv', sound_path], stdout=PIPE, stderr=PIPE)

		#? don't block, continue executing while playing
		else:
			Popen(['mpv', sound_path], stdout=PIPE, stderr=PIPE)

	else:
		raise FileNotFoundError(f"'{sound_path}' does not exist")

