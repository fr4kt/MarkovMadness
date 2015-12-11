A small collection of Markov Chain based projects.

markovMusic.py is a script that automatically generates music based off of a predetermined markov chain for the duration and pitch of notes. I'm in the process of modifying it to use explicit transtion matrices rather than the cryptic probability munging it does now.

Future adds:
	Selecting notes in larger groups
	Support for individual scales
	Support for non-western scales
	Support for training sets of music to generate new

markovViz.py is a very simple class for vizualizing how a Markov Chain evolves. The nodes are lined up vertically and the horizontal axis is time. The class methods proved a way to modify the chain while it's running which could make for some interesting results.
