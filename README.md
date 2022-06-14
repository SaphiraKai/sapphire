## Sapphire - a simple, actually helpful personal assistant leveraging Google Speech Recognition and GPT-3, for programmers

This is the evolution of a much older and much dumber project I wrote a long time ago, never published.

At current, Sapphire only runs on Linux, and theoretically BSD and macOS. If there's demand for Windows compatibility, I'll add it...

### Unfortunately, this project requires an OpenAI API key!
If I could change it I would, but sadly you'll need to sign up with OpenAI and get your own API key to make this work.

Fortunately, OpenAI currently gives you USD$18 of API credit (enough for roughly a few weeks of Sapphire, depending on usage) for free when you sign up, and thankfully doesn't ask for your info!

Assuming that isn't a dealbreaker, go ahead and make an account with OpenAI (email and password): https://beta.openai.com/signup

Once that's done, open the menu in the top right and go to 'View API keys'. Copy your key, then run the following command:
```
printf '\nexport OPENAI_KEY="your api key here"\n' >> ~/.${SHELL}rc
```
This will create an environment variable containing your API key. Make sure nobody potentially malicious has read access to your shell rc file!

Once that's done, Sapphire should use that key and you'll be all set!

## Installation
Make sure you set up your API key as explained above.

#### Arch Linux / derivatives
```
git clone https://github.com/SaphiraKai/sapphire
cd sapphire
./tar.sh
makepkg -csi
```

#### Other distributions
Ensure you have the necessary dependencies installed:
```
bash
python
python-openai            / pip 'openai'
python-speechrecognition / pip 'SpeechRecognition'
mpv
```

Then you can run the following commands:
```
git clone https://github.com/SaphiraKai/sapphire
cd sapphire
sudo ./install.sh
```

## Usage
Using Sapphire is pretty simple! Run `$ sapphire` in a terminal, it will briefly adjust for ambient noise, and then simply ask a question or state a request.

You can exit by speaking one of the trigger phrases, 'exit', 'nevermind', 'cancel', and 'that's all' are noteworthy. It's likely the database will be greatly expanded over time, so check out `data.py` to see them all!

Similarly, you can confirm running a shell command with 'yes', 'confirm', 'continue' etc.

Some of the things it can do pretty well are:
- Run complex-ish shell commands for you (Run a command to list the top 5 CPU consuming processes.)
- Install some software for you (Install LibreOffice.)
- Write some code for you (Write a function in Python to add two numbers together.)
- Answer questions (What are the benefits of using Rust over C++?)
- Impress the hell out of your friends (Write a short story about \<friend1\> and \<friend2\>.)

There are of course some things that Sapphire doesn't do very well at the moment.
For example, when writing shell commands, Sapphire has no way of knowing what shell you're using, or what software you have installed. This means it will sometimes make incorrect assumptions and generate a command that doesn't run on your machine, though I haven't found this to happen terribly often.

A related problem is that it doesn't *always* understand context properly, and it might try to run a command without sudo even if it would fail without root privileges.

On the plus side, the AI engine is given the name of your OS, which can greatly help its ability to generate correct commands in certain situations, especially ones involving the package manager!
