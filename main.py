#!/usr/bin/env python3

import openai
import os
import subprocess
import speech_recognition as sr
from sys import stdout

import functions
import errors
import colors
import voice


openai.api_key = os.environ['OPENAI_KEY']

r =	sr.Recognizer()
m = sr.Microphone()

print("\033[2J", end='')

with m as source:
	print("calibrating for ambient noise...")
	r.adjust_for_ambient_noise(source)

print("\033[2J", end='')

log = open('/tmp/sapphire.log', 'w')

reply            = ""
request          = ""
previous_reply   = reply
previous_request = request
while True:
	log.write(request + reply + '\n\n')

	previous_request = request + '\n\n'
	previous_reply = reply + '\n\n'

	with m as source:
		voice.play("listening")
		print(colors.cyan + "listening: " + colors.reset, end='')
		stdout.flush()
		audio =	r.listen(source)

	try:
		recognized = r.recognize_google(audio)
		request = functions.punctuate(recognized)
		print(colors.bright_yellow + request + colors.reset + '\n')

	except sr.UnknownValueError:
		print('\n\n' + errors.recognize + '\n')
		voice.play('error', block=True)
		continue

	except sr.RequestError as e:
		print('\n\n' + errors.request + e)
		voice.play('error', block=True)
		log.close()
		functions.exit()

	if recognized in ['nevermind', 'cancel', 'exit', 'done', "that's it", "that's all", "that'll be all"]:
		log.close()
		functions.exit()

	else:
		voice.play('processing')

	request = functions.punctuate(recognized)

	prompt = f"If you don't understand, say only 'ERROR'.\n\nIf you run a shell command, prepend it with '$ '.\nExample: $ echo 'hello world'\n\nIf you are asked to 'write', write a program with the given function in the given language.\n\nInformation about the system:\nOS: Arch Linux\n\n" + previous_request + previous_reply + request

	if request != '':
		response = openai.Completion.create(
			engine="text-davinci-002",
			prompt=prompt,
			max_tokens=512,
			temperature=0,
			top_p=1,
		)

		reply =	response.choices[0].text.rstrip().replace('\n\n', '\n')

		if 'ERROR' in reply or reply == '':
			print(errors.clarity + '\n')
			voice.play('error', block=True)

		elif reply.lstrip()[:2] == '$ ':
			cmd = reply.lstrip()[2:].split('\n')[0]

			with m as source:
				voice.play('confirm')
				print(colors.cyan + "confirm:" + colors.magenta, cmd, end='')
				stdout.flush()
				audio =	r.listen(source)

			try:
				if r.recognize_google(audio) in ['yes', 'yep', 'yup', 'confirm', 'continue']:
					print(colors.blue+"\033[0G//// running" + colors.magenta, cmd + colors.reset)
					subprocess.call(["bash", "-c", cmd])
					print(colors.blue+r"\\\\ finished")

				else:
					print('\033[0G')

			except sr.UnknownValueError:
				print('\n\n' + errors.recognize + '\n')
				voice.play('error', block=True)
				continue

			except sr.RequestError as e:
				print('\n\n' + errors.request + e)
				voice.play('error', block=True)
				log.close()
				functions.exit()

			print()

		else:
			print(colors.reset + request + colors.magenta + reply + '\n')
