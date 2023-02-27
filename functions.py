#// global modules \\\\\\\\#
import openai
from sys import stdout
import speech_recognition as sr
from subprocess import call
#\\\\\\\\ global modules //

#// local modules \\\\\\\\#
import voice
import errors
import colors
import data
import cursor
import config.complete
#\\\\\\\\ local modules //#

#// functions \\\\\\\\#
#? play the exit sound and then quit
def exit():
	voice.play("exit", True)
	quit()


#? get the name of the distribution from /etc/os-release
def get_os():
	with open('/etc/os-release', 'r') as f:
		for key in f.read().splitlines():
			if key[:4] == 'NAME':
				os = key.split('=')[1]

	return os


#? generate a prompt header, containing useful information for the completion
#  engine to know
def get_header():
	return data.header.format(operating_system=get_os())


#? add punctuation to requests based on whether it's a question or instruction
def punctuate(statement):
	if statement.split()[0] in data.questions:
		statement += '?'

	else:
		statement += '.'

	return statement


#? calibrate for ambient noise level
def calibrate(m, r):
	with m as source:
		print("calibrating for ambient noise...")
		r.adjust_for_ambient_noise(source)

	return r.energy_threshold


#? use speech recognition or keyboard input to get a request from the user
def listen(m, r, use_keyboard):
	if use_keyboard:
		voice.play("listening")
		request = input(colors.cyan + "enter request: " + colors.bright_yellow)
		print(colors.reset)

		return request

	else:
		#? listen
		with m as source:
			voice.play("listening")
			print(colors.cyan + "listening: " + colors.reset, end='')
			stdout.flush()
			audio =	r.listen(source)

		#? attempt to return request
		try:
			recognized = r.recognize_google(audio)
			request = punctuate(recognized)
			print(colors.bright_yellow + request + colors.reset + '\n')

			return request

		#? didn't understand audio
		except sr.UnknownValueError:
			print('\n\n' + errors.recognize + '\n')
			voice.play('error', block=True)

		#? unable to contact api
		except sr.RequestError as e:
			print('\n\n' + errors.request + e)
			voice.play('error', block=True)


#? prompt the user to confirm, then execute a shell command
def run_command(m, r, cmd, use_keyboard):
	if use_keyboard:
		voice.play('confirm')
		confirmation = input(colors.cyan + "confirm (y/N): " + colors.magenta)
		print(colors.reset, end='')
		
		if confirmation.lower() in ['y', 'yes']:
			print(colors.blue + cursor.line_start + "//// running" + colors.magenta, cmd + colors.reset)
			call(["bash", "-c", cmd])
			print(colors.blue + r"\\\\ finished")
		
		else:
			print()
		
	else:
		with m as source:
			voice.play('confirm')
			print(colors.cyan + "confirm:" + colors.magenta, cmd, end='')
			stdout.flush()
			audio =	r.listen(source)

		#? attempt to confirm and run command
		try:
			recognized = r.recognize_google(audio)
			if recognized in data.confirmations:
				print(colors.blue + cursor.line_start + "//// running" + colors.magenta, cmd + colors.reset)
				call(["bash", "-c", cmd])
				print(colors.blue + r"\\\\ finished")

			else:
				print()

		#? didn't understand audio
		except sr.UnknownValueError:
			print('\n\n' + errors.recognize + '\n')
			voice.play('error', block=True)

		#? unable to contact api
		except sr.RequestError as e:
			print('\n\n' + errors.request + e)
			voice.play('error', block=True)

			return False

		print()
		return True


#? check whether the user has requested to exit
def should_exit(request):
	if request in data.exit_requests:         return True
	elif request + '.' in data.exit_requests: return True
	else:                                     return False


#? request a completion of the given prompt
def complete(m, r, request, prompt, use_keyboard):
	#? request completion
	response = openai.Completion.create(engine=config.complete.engine,
										prompt=prompt,
										max_tokens=config.complete.max_tokens,
										temperature=config.complete.temperature,
										top_p=config.complete.top_p)

	#? parse and clean up reply
	reply =	response.choices[0].text.rstrip().replace('\n\n', '\n')

	#? engine didn't understand the prompt, request clarification from the user
	if 'ERROR' in reply or reply == '':
		print(errors.clarity + '\n')
		voice.play('error', block=True)

	#? check if reply is a shell command to be executed
	elif reply.lstrip()[:2] == '$ ':
		cmd = reply.lstrip()[2:].split('\n')[0]
		run_command(m, r, cmd, use_keyboard)
		return '$ ' + cmd

	#? print reply from the engine
	else:
		print(colors.reset + request + colors.magenta + reply + '\n')
		return reply
#\\\\\\\\ functions //#
