# Sloviet Blaseball

A convenient method to securely transmit encrypted Blaseball game updates to
agents in the field.

An entry for the [2021 SIBR "Snackathon"](https://cursed.sibr.dev/) (hackathon).

## What Is It?

Sloviet Blaseball is a numbers station generator that creates a broadcast-ready
audio signal containing an encrypted play-by-play of a given Blaseball game.
The encrypted game is rendered as a series of messages consisting of partially
randomized digits, which are in turn read out using prerecorded audio of a
person speaking each digit. This audio signal can be recorded, played through
your computer's audio system, and/or piped into a radio transmitter for maximum
authenticity (and potential illegality depending on your location).

## Installation and Setup

### Requirements

Sloviet Blaseball is written in Python and should run on all systems supporting
**Python 3.8 and up**. If you don't have access to Python 3.8 or above, or if
you frequently develop using multiple Python versions and virtualenvs, you may
want to check out [Pyenv](https://github.com/pyenv/pyenv).

### Installation

1.  Clone this repository locally
    ```sh
    git clone https://github.com/malorisdead/SlovietBlaseball.git
    ```
2.  Create and activate a virtual environment
    ```sh
    cd SlovietBlaseball
    python -m venv venv
    . venv/bin/activate
    ```
    If you're using Pyenv, all you need to do is create a virtualenv named
    `sloviet`. Pyenv should automatically activate it for you when you enter
    the project directory (if you're using an older version, you may need to
    install the [Pyenv virtualenv](https://github.com/pyenv/pyenv-virtualenv)
    plugin first).
    ```sh
    pyenv virtualenv 3.8.10 sloviet
    ```
    **Windows Users**: to activate a virtualenv, you'll need to run:
    ```sh
    venv/Scripts/activate.bat
    ```
3.  Install required packages
    ```sh
    pip install -r requirements.txt
    ```

That's it!

### Setup

In order to set up the application to run correctly, you will need to generate
some one-time pads that will be used to encrypt messages. Currently, this step
is not optional, but luckily it is simple. Simply run:

```sh
./generate-otp.py
```

This will create a new file, `otp.txt`, in the root directory of the repository.
Once that's done, you're ready to run!

## Running

Sloviet Blaseball produces a raw audio signal on the standard output. To run
Sloviet Blaseball effectively, you will need to pipe its output to a suitable
destination.

Note: I have only tested this on Linux. Your mileage may vary.

### CLI

The Sloviet Blaseball command line takes three possible arguments.

- `-s` or `--skip-headers`: passing this flag will cause Sloviet Blaseball to
  not send RIFF header bytes for each digit it sends. This flag is recommended
  for use with destinations such as `play` or `sox` which play audio through
  the connected speakers or record audio to a file. A header will still be sent
  as the application starts up, but only raw audio bytes will be sent thereafter.

  **Note:** this flag is optional.

- `-t` or `--text-only`: passing this flag will skip the audio output entirely,
  and instead all encrypted messages will be printed to standard output. This
  is mostly useful for debugging purposes.

  **Note:** this flag is optional; if passed, the `-s` flag is ignored as it is
  meaningless.

- The game ID, as a plain GUID.

  **Note:** this argument is required.

### Example Usage: Playing Audio

To play Sloviet Blaseball's output directly through your current speakers using
the `play` command on Linux:

```sh
./sloviet.py --skip-headers 1bf2ec1a-4df8-4446-b7f0-55ba901d4f30 | play -Gq -t wav --ignore-length -
```

**Notes:** the `--ignore-length` is necessary here. Sloviet Blaseball does not
constantly fill the output buffer with silent audio bytes. By default, `play`
will interpret the first null byte it finds as an EOF and terminate play.

### Example Usage: An FM Numbers Station with a Raspberry Pi

<span style="color:red">**IMPORTANT NOTE:**</span> FM radio is a licensed band
in most countries, meaning that broadcasting on FM frequencies without a license
is likely illegal. Familiarize yourself with local laws and regulations around
FM radio broadcasting, and proceed at your own risk!

Now, with that in mind, here in the US low-power unlicensed FM broadcasts
[are generally permitted](https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=1&SID=aad0dee9d5dd560e44f29c7d58918f9d&h=L&mc=true&n=pt47.1.15&r=PART&ty=HTML#se47.1.15_15),
provided they don't interfere with any licensed transmissions or any other
electronic devices, so I include the following instructions with the intention
that they be used only in accordance with any such laws. Most importantly, I am
not a lawyer, so don't believe anything I say and look up the law yourself.

If you have taken heed of the above warnings, familiarized yourself with all
of your local and national laws, and still want to proceed, then luckily there
are several projects that will allow you to easily turn an ordinary Raspberry Pi
into a local low-power FM transmitter. The only requirement for having it work
with Sloviet Blaseball is that it accept data through standard input.

The original project by Oliver Mattos and Oskar Weigl is [here](http://www.icrobotics.co.uk/wiki/index.php/Turning_the_Raspberry_Pi_Into_an_FM_Transmitter).
You can also use [this one](https://github.com/mundeeplamport/PiFM) if you want
something with a GUI.

I used the original PiFM and a Raspberry Pi 3 Model B to test:

```sh
./sloviet.py 1bf2ec1a-4df8-4446-b7f0-55ba901d4f30 | sudo ./pifm - 88.5 22050
```

Note that for some Raspberry Pi FM transmitter apps, you do _not_ want to pass
the `--skip-headers` flag. They expect a new WAV header for every block of data.

Remember to use a service like [radio-locator](http://radio-locator.com/cgi-bin/vacant)
to find a frequency in your area where you won't interfere with a licensed
transmitter.

## Theory of Operation

Sloviet Blaseball operates by querying the Blaseball API for general game
information and [Chronicler](https://docs.sibr.dev/docs/apis/reference/Chronicler.v1.yaml)
to retrieve the play-by-play for a game. Currently, it does not work with live
games on blaseball.com, but this may be achievable in the future.

### Software Architecture

This block diagram was recently declassified, from old East German records.<sup>1</sup>
It roughly describes the software architecture of Sloviet Blaseball.

![Block diagram](block-diagram.jpg?raw=true)

### Application Output

Sloviet Blaseball outputs an audio stream in the form of raw WAV PCM bytes.
The output is directed to the standard output file and is pipeable.

If used with the `--skip-headers` flag, Sloviet Blaseball will send a single
WAV RIFF header of 44 bytes before waiting until message data is available to
transmit. This may cause unexpected behavior in downstream applications which
interpret null bytes as end-of-file indicators.

If used without the flag, the output is a stream consisting of multiple WAV
files complete with headers.

### Transmission Format

Sloviet Blaseball attempts to imitate the functionality of a genuine numbers
station. In order to do so, messages must be encoded as numeric digits. To
accomplish this, Sloviet Blaseball uses a [straddling checkerboard encoder](https://en.wikipedia.org/wiki/Straddling_checkerboard),
which has a number or number combination that corresponds to each letter in a
message, as well as special short codes that indicate certain message types.
For all other message types, the event type ID is converted to a three-digit
code when present; otherwise, the full message text is encoded.

![The Blaseball Checkerboard](blaseboard.png?raw=true)

**R/H** indicates "runs/home," the home team score; **R/A** runs/away, the away
team score. **FIG** stands for "figure" and is used to indicate that the digits
that follow it are to be interpreted as numbers and not as checkerboard codes,
until another FIG code is found. Some ambiguity may arise from numbers that
include the figure code (99 in this checkerboard) but context should aid the
agent in decoding the message correctly. **CODE** is used to prefix the
three-digit event type codes; for a list of these, please refer to the
[Blaseball Wiki](https://www.blaseball.wiki/w/SIBR:Feed#Event_types).

Once the message is encoded into digits using the checkerboard, it is then
encrypted using a [one-time pad](https://en.wikipedia.org/wiki/One-time_pad) to
supply the key. This repository includes a script that will generate one-time
pads in the correct format. Each pad is a series of five-digit groupings of
numbers. The first five-digit group is the pad identifier, while the rest are
the key. The digits of the key are aligned with the digits of the encoded
message, and subtracted one digit at a time, modulo 10 (see the wiki for more
details). The message is then padded with zeros at the end until it reaches a
length divisible by 5.

The final message is then composed of the pad identifier digits (unencrypted),
the encrypted message digits in groups of five, and three zeroes (unencrypted).

To begin the transmission and indicate useful data to agents in the field, the
first thing Sloviet Blaseball transmits is an identifier: its own agent ID
(currently, just the process ID of the script) repeated three times, the group
ID of the transmission (the season number of the Blaseball game) repeated twice,
and the group count of the transmission (the day of the Blaseball game). The
group ID is padded to three digits with preceding zeroes. The group count is
padded to two digits, but may be three digits for postseason games.

The first message sent will then be an overview of the game, indicating the
home and away teams and the weather, if any. The next message will indicate the
pitchers for each team. The following messages will each be a play-by-play from
the game feed as found on blaseball.com.

### The Reader (Not That One)

Once a transmission is encoded and encrypted, it is converted to audio by
an extremely simple text-to-speech engine. Again based on genuine numbers
stations, Sloviet Blaseball loads a recording of a person reading each number
from zero through nine into memory and splices them together dynamically to
generate its output. These recordings can be found in the `audio` directory.

It is possible to replace these audio recordings with custom ones. Simply
provide a separate file for each digit, 0.75 seconds in length, encoded as a
monaural WAV file at 22050Hz.

### Example Transmission

To summarize the above, the following is an example of a Sloviet Blaseball
transmission, with annotations:

```
2135  2135  2135
Agent ID, three times

004  004
Season, two times

108  108
Day, two times

43742 11257 66480 59060 90661 64007 75239 48047 97212 28750 63980 61823  0 0 0
Pad   Away team: Millennials, Home team: Firefighters, Weather: Feedback End message

88773 05845 51367 93125 18856 71161 65004 85007 18053 25996 0 0 0
Pad   Pitching: Finn Doyle (A) vs. Axel Trololol (H)        End message

...

53990 57265 23762 72884 0 0 0
Pad   Thomas Dracaena hit a ground out to Edric Tosser End message
```

### Example Message

To illustrate the process of decryption, let's take a look at one of the above
messages.

```
43742 11257 66480 59060 90661 64007 75239 48047 97212 28750 63980 61823  0 0 0
```

This message signals the start of the game. It is broken into five-digit groups,
starting with the ID of the one-time pad used to perform the encryption, and
ending with three zeroes.

To decrypt this message, first an agent needs to locate the specific one-time
pad in their copy of the pads distributed prior to their assignment. These
must match the pads used by Sloviet Blaseball to perform the encryption;
otherwise, the messages are completely unbreakable.

Once the relevant pad is identified by its first group of five, the agent lines
the rest of the digit groups up with the rest of the digit groups in the message.
The zeroes that terminate the message are ignored.

```
43742 11257 66480 59060 90661 64007 75239 48047 97212 28750 63980 61823 (message)
43742 99851 80485 73509 79092 60839 51344 18228 76435 27084 47381 68187 (one-time pad)
```

The message is encrypted by subtracting each digit modulo 10, so the encryption
is reversed by adding each digit modulo 10 (ignoring the pad identifier):

```
43742 11257 66480 59060 90661 64007 75239 48047 97212 28750 63980 61823
43742 99851 80485 73509 79092 60839 51344 18228 76435 27084 47381 68187
      00008 46865 22569 69653 24836 26573 56265 63647 45734 00261 29900
```

The message can now be decoded using the straddling checkerboard. Any trailing
zeroes at the end are usually padding and can be discarded. The grouping into
five-digit blocks can also be ignored, and the string of digits interpreted
straight through.

```
00008 46865 22569 69653 24836 26573 56265 63647 45734 00261 29900
0    000  84   68 65 2 2 5 69 69 65 3 2 4 83   62 65 73 5 62 65 63 64 74 5 73 4 0    026     12 99
Code Game Away M  I  L L E N  N  I  A L S Home F  I  R  E F  I  G  H  T  E R  S Code Weather Feedback
```

Note that certain codes can be followed by numbers without a FIGURE code (99).
This is done to shorten messages as much as possible. The Weather code (026)
in this message is a good example; other examples include the codes for the
home and away scores, counts of balls, strikes, and outs, and the inning change
codes. These raw digits will still be followed by a FIGURE code indicating that
there are no more numbers, and the agent can resume interpreting codes as usual.
Also note that certain elements such as weather, stadium, and tarot cards are
transmitted by their ID number; agents will need to refer to the latest tables
to interpret these correctly.

## Final Notes

As mentioned previously, once a one-time pad is generated it must be shared with
all agents who are expected to receive your transmissions. If distributing in
print, it is recommended to format each line of the generated file into its own
page for ease of recovery (as each line is considered one pad, and its first
digit group is its identifier). Agents are reminded to destroy each pad after
use; administrators are reminded to generate a new OTP file before each use of
the software. One-time pads are unbreakable when used once, but repeat usage
increases the likelihood of malicious actors cracking your encryption.

## To-Do List

- [ ] Actually delete one-time pads after usage (includes regeneration, possibly)
- [ ] Better audio handling (somewhat limited by PiFM transmitter input reqs)
- [ ] More custom event handling
- [ ] Better error handling
- [ ] Postseason games
- [ ] ████████████
- [ ] Other unusual situations

## Acknowledgments

The original idea for doing this project in particular comes from my wonderful
wife Ilona. One of her first suggestions when I mentioned the hackathon theme
was a numbers station and that is among the many reasons why I love her.

Obviously this project owes a great deal to the wonderful witches of [SIBR](https://sibr.dev).
Particular thanks to [ch00beh](https://github.com/jmaliksi) for their extremely
useful [blaseball-mike](https://github.com/jmaliksi/blaseball-mike) library.

The Voice of Sloviet Blaseball is remixed from an audio clip provided by Timbre
over on [Freesound.org](https://freesound.org/s/408138/), which I sliced, diced,
and modified (slightly) to create the sounds found in this repo. The audio is
licensed CC-By-NC; please do not reupload these clips without proper attribution.

Major inspiration for this project comes from [linuxcoffee.com](https://linuxcoffee.com/numbers/)
and their page on a similar project. A big shoutout goes to [Dirk Rijmenants](http://users.telenet.be/d.rijmenants/index.htm)'
extensive website about different cryptographic techniques.

And, of course, none of this would be possible without The Game Band and their
weird and wonderful brainchild [Blaseball](https://www.blaseball.com).

<span style="background-color: black;color: black;">LGMBLDM!</span>

---

## Endnotes

[1]: This is not true
