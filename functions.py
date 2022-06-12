import openai
from sys import stdout
import speech_recognition as sr
from subprocess import call

import voice
import errors
import colors
import data
import cursor
import config.complete

def exit():
	voice.play("exit")
	quit()

def get_os():
	with open('/etc/os-release', 'r') as f:
		for key in f.read().splitlines():
			if key[:4] == 'NAME':
				os = key.split('=')[1]

def get_header():
	return data.header.format(operating_system=get_os())

def punctuate(statement):
	if statement.split()[0] in data.questions:
		statement += '?'

	else:
		statement += '.'

	return statement

def calibrate(m, r):
	with m as source:
		print("calibrating for ambient noise...")
		r.adjust_for_ambient_noise(source)

	return r.energy_threshold

def listen(m, r):
	with m as source:
		voice.play("listening")
		print(colors.cyan + "listening: " + colors.reset, end='')
		stdout.flush()
		audio =	r.listen(source)

	try:
		recognized = r.recognize_google(audio)
		request = punctuate(recognized)
		print(colors.bright_yellow + request + colors.reset + '\n')

		return request

	except sr.UnknownValueError:
		print('\n\n' + errors.recognize + '\n')
		voice.play('error', block=True)

	except sr.RequestError as e:
		print('\n\n' + errors.request + e)
		voice.play('error', block=True)
		return ''

def run_command(m, r, cmd):
	with m as source:
		voice.play('confirm')
		print(colors.cyan + "confirm:" + colors.magenta, cmd, end='')
		stdout.flush()
		audio =	r.listen(source)

	try:
		recognized = r.recognize_google(audio)
		if recognized in data.confirmations:
			print(colors.blue + cursor.line_start + "//// running" + colors.magenta, cmd + colors.reset)
			call(["bash", "-c", cmd])
			print(colors.blue + r"\\\\ finished")

		else:
			print()

	except sr.UnknownValueError:
		print('\n\n' + errors.recognize + '\n')
		voice.play('error', block=True)

	except sr.RequestError as e:
		print('\n\n' + errors.request + e)
		voice.play('error', block=True)

		return False

	print()
	return True

def should_exit(request):
	if request in data.exit_requests: return True
	else:                             return False


def complete(m, r, request, prompt):
	response = openai.Completion.create(engine=config.complete.engine,
										prompt=prompt,
										max_tokens=config.complete.max_tokens,
										temperature=config.complete.temperature,
										top_p=config.complete.top_p)

	reply =	response.choices[0].text.rstrip().replace('\n\n', '\n')

	if 'ERROR' in reply or reply == '':
		print(errors.clarity + '\n')
		voice.play('error', block=True)

	elif reply.lstrip()[:2] == '$ ':
		cmd = reply.lstrip()[2:].split('\n')[0]
		run_command(m, r, cmd)

	else:
		print(colors.reset + request + colors.magenta + reply + '\n')
