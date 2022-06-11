#!/usr/bin/env python3

import openai
import os
import subprocess
import speech_recognition as sr
from sys import stdout


openai.api_key = os.environ['OPENAI_KEY']

black          = '\033[30m'
red            = '\033[31m'
green          = '\033[32m'
yellow         = '\033[33m'
blue           = '\033[34m'
magenta        = '\033[35m'
cyan           = '\033[36m'
white          = '\033[37m'
bright_black   = '\033[30;1m'
bright_red     = '\033[31;1m'
bright_green   = '\033[32;1m'
bright_yellow  = '\033[33;1m'
bright_blue    = '\033[34;1m'
bright_magenta = '\033[35;1m'
bright_cyan    = '\033[36;1m'
bright_white   = '\033[37;1m'
reset          = '\033[0m'

r =	sr.Recognizer()
m = sr.Microphone()

print("\033[2J")

with m as source:
	print("calibrating for ambient noise...")
	r.adjust_for_ambient_noise(source)

print("\033[2J")

reply            = ""
request          = ""
previous_reply   = reply
previous_request = request
while True:
	with m as source:
		print(cyan+"listening: ", end='')
		stdout.flush()
		subprocess.call(['mpv', '/usr/share/sounds/freedesktop/stereo/window-question.oga'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		audio =	r.listen(source)

	try:
		recognized = r.recognize_google(audio)
		print(bright_yellow+recognized, end=reset+'\n\n')

	except sr.UnknownValueError:
		print(f"\n\n{bright_red}error: unable to recognize speech\n")
		continue

	except sr.RequestError as e:
		print(f"\n\n{bright_red}error: unable to request results from Google Speech Recognition service: {0}\n".format(e))
		exit()

	if recognized in ['cancel', 'exit', 'done', "that's it", "that's all"]:
		exit()

	if request != '': previous_request = request + '\n\n'
	request = recognized

	prompt = f"If you don't understand, say only 'ERROR'.\nIf you run a shell command, prepend it with '$ '.\nExample: $ echo 'hello world'\nIf you are asked to 'write', write a program with the given function in the given language.\n\nInformation about the system:\nOS: Arch Linux\n\n" + previous_request + previous_reply + request

	if request != '':
		response = openai.Completion.create(
			engine="text-davinci-002",
			prompt=prompt,
			max_tokens=512,
			temperature=0,
			top_p=1,
		)

		if reply != '': previous_reply = reply + '\n\n'
		reply =	response.choices[0].text.rstrip().replace('\n\n', '\n')

		if 'ERROR' in reply or reply == '':
			print(f"{bright_red}error: {reset}please clarify\n")

		elif reply.lstrip()[:2] == '$ ':
			cmd = reply.lstrip()[2:].split('\n')[0]

			with m as source:
				print(cyan+"confirm:"+magenta, cmd, end='')
				stdout.flush()
				subprocess.call(['mpv', '/usr/share/sounds/freedesktop/stereo/window-question.oga'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				audio =	r.listen(source)

			try:
				if r.recognize_google(audio) in ['yes', 'yep', 'yup', 'confirm', 'continue']:
					print(blue+"\033[0G//// running"+magenta, cmd+reset)
					subprocess.call(["bash", "-c", cmd])
					print(blue+r"\\\\ finished")

			except sr.UnknownValueError:
				print(f"\n\n{bright_red}error: {reset}unable to recognize speech\n")
				continue

			except sr.RequestError as e:
				print(f"\n\n{bright_red}error: {reset}unable to request results from Google Speech Recognition service: {0}\n".format(e))
				exit()

			if recognized in ['cancel', 'exit', 'done', "that's it", "that's all"]:
				exit()

			print()

		else:
			print(reset+request + magenta+reply + '\n')
