#? prompt header template
header = """If you don't understand, say only 'ERROR'.

If you are asked to do something, run a shell command to do it.
Example: get the current time.
Response: $ date

If you run a shell command, prepend it with '$ '.
Example: $ echo 'hello world'
Example: $ for i in *; do echo "found $i"; done

If you are asked to 'write', write a function with the given purpose in the given language with 'CODE' as the first line.
Do not surround it with backticks.
Example: Write a Rust function to add two numbers together.
Response:
CODE
fn add(a: usize, b: usize) -> usize {{
	return a + b;
}}


Information about the system:
OS = {operating_system}

"""

#? words that start questions
questions = ['is',
             'can',
             'could',
             'had',
             'has',
             'have',
             'how',
             'should',
             'will',
             'what',
             'when',
             'where',
             'who',
             'why',
             'would']

#? requests to exit
exit_requests = ['all right thank you.',
				 'alright thank you.',
	             'okay thank you.',
	        	 'thank you.',
				 'nevermind.',
	             'cancel.',
	             'exit.',
	             'done.',
	             "that's it.",
	             "that's all.",
	             "that'll be all."]

#? confirmations to perform an action
confirmations = ['yes',
                 'yep',
                 'yup',
                 'confirm',
                 'continue']

