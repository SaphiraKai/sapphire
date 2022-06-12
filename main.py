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


def main():
	openai.api_key = os.environ['OPENAI_KEY']

	operating_system = functions.get_os()


	r =	sr.Recognizer()
	m = sr.Microphone()

	print("\033[2J", end='')

	r.pause_threshold  = 0.5
	r.energy_threshold = functions.calibrate(m, r)

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

		request = functions.listen(m, r)

		if functions.should_exit(request):
			break

		else:
			voice.play('processing')

		prompt = functions.get_header() + previous_request + previous_reply + request

		if request != '':
			functions.complete(m, r, request, prompt)

	log.close()
	functions.exit()

if __name__ == '__main__':
	main()
