#? prompt header template
header = """If you don't understand, say only 'ERROR'.

If you run a shell command, prepend it with '$ '.
Example: $ echo 'hello world'
Example: $ for i in *; do echo "found $i"; done

If you are asked to 'write', write a program with the given function in the given language.

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
exit_requests = ['nevermind.',
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

