import voice

questions = ['is', 'can', 'how', 'will', 'what', 'when', 'where', 'who', 'why']

def exit():
	voice.play("exit")
	quit()

def punctuate(statement):
	if statement.split()[0] in questions:
		statement += '?'

	else:
		statement += '.'

	return statement
