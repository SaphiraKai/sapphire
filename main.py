#!/usr/bin/env python3

#// global modules \\\\\\\\#
import openai
import os
import speech_recognition as sr
#\\\\\\\\ global modules //#

#// local modules \\\\\\\\#
import functions
import errors
import colors
import voice
import cursor
#\\\\\\\\ local modules //#


def main():
	openai.api_key = os.environ['OPENAI_KEY']

	#? get name of distribution from /etc/os-release
	operating_system = functions.get_os()


	#? initialize the microphone and speech recognition engine
	r =	sr.Recognizer()
	m = sr.Microphone()

	print(cursor.clear, end='')

	#? shorten pause_threshold from 0.8s to 0.5s
	r.pause_threshold  = 0.5

	#? calibrate for ambient noise level
	r.energy_threshold = functions.calibrate(m, r)

	print(cursor.clear, end='')


	#? start logging the current conversation, overwriting the previous
	log = open('/tmp/sapphire.log', 'w')

	#? initialize variables
	reply            = ''
	request          = ''
	previous_reply   = reply
	previous_request = request


	#// main loop \\\\\\\\#
	while True:
		if request != None:
			log.write(request + reply + '\n\n')

			previous_request = request + '\n\n'
			previous_reply = reply + '\n\n'

		#? use speech recognition to prompt the user for a request
		request = functions.listen(m, r)

		#? check if the user has requested to exit
		if functions.should_exit(request):
			break

		#? getting the request failed, restart the loop
		elif request == None:
			continue

		#? play processing sound
		else:
			voice.play('processing')

		#? generate the prompt to send to OpenAI
		prompt = functions.get_header() + previous_request + previous_reply + request

		#? request a completion of the prompt and perform any necessary actions
		if request != '':
			functions.complete(m, r, request, prompt)

	#? stop logging and exit with the exit sound
	log.close()
	functions.exit()
	#\\\\\\\\ main loop //#

#? run main()
if __name__ == '__main__':
	main()
