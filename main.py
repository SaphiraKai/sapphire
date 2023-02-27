#!/usr/bin/env python3

#// global modules \\\\\\\\#
import argparse
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

#// argument parsing \\\\\\\\#
parser = argparse.ArgumentParser(description='Sapphire - A simple, actually helpful personal assistant leveraging Google Speech Recognition and GPT-3, for programmers')
parser.add_argument('-c', '--calibrate', action='store_true', help="Calibrate for ambient noise on startup")
parser.add_argument('-k', '--keyboard', action='store_true', help="Use keyboard input instead of speech recognition")

args = parser.parse_args()
#\\\\\\\\ argument parsing //#


def main():
	openai.api_key = os.environ['OPENAI_KEY']

	cache_path = os.path.expanduser('~') + '/.cache/sapphire/' 
	
	#? get name of distribution from /etc/os-release
	operating_system = functions.get_os()


	#? initialize the microphone and speech recognition engine
	r =	sr.Recognizer()
	m = sr.Microphone()

	print(cursor.clear, end='')

	#? shorten pause_threshold from 0.8s to 0.5s
	r.pause_threshold  = 0.5

	
	#? calibrate for ambient noise level
	if not args.keyboard:
		if not os.path.exists(cache_path + 'noise_calibration'):
			try:
				os.makedirs(cache_path)
			except:
				None

			r.energy_threshold = functions.calibrate(m, r)
			with open(cache_path + 'noise_calibration', "w") as f:
				f.write(str(r.energy_threshold))

		if args.calibrate:
			r.energy_threshold = functions.calibrate(m, r)
			with open(cache_path + 'noise_calibration', "w") as f:
				f.write(str(r.energy_threshold))

		else:
			with open(cache_path + 'noise_calibration', 'r') as f:
				r.energy_threshold = float(f.readline())

	
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
			log.write(request + '\n' + reply + '\n\n')

			previous_request = request + '\n\n'
			previous_reply = reply + '\n\n'

		#? use speech recognition to prompt the user for a request
		request = functions.listen(m, r, args.keyboard)

		#? getting the request failed, restart the loop
		if request == None:
			continue

		#? check if the user has requested to exit
		elif functions.should_exit(request):
			break

		#? play processing sound
		else:
			voice.play('processing')

		#? generate the prompt to send to OpenAI
		prompt = functions.get_header() + previous_request + previous_reply + request

		#? request a completion of the prompt and perform any necessary actions
		if request != '':
			try:
				reply = functions.complete(m, r, request, prompt, args.keyboard)
			except KeyboardInterrupt:
				continue
		
		if reply == None:
			reply = ''

	#? stop logging and exit with the exit sound
	log.close()
	functions.exit()
	#\\\\\\\\ main loop //#

#? run main()
if __name__ == '__main__':
	main()
