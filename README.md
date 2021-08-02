# Pymusic 
Here I provide a simple code that generate notes.
I basically generate a sine function with a given frequency and with a few calculations make that sound just nice as you would expect from a keyboard.
Here is your digital music producer. I currently generate a song with frequencies following a route to chaos in logistic map !

PS: This code was done under python2. If you are python3 user you will face issues with scitools.sound, see next step for that.
Next steps:
- Fix scitools_sound.py this is a python2 implementation of scitools.sound lib . One could modify it to run over python3
- Real world sounds are not perfec sine functions. Lets define a gaussian distribution around each note and then creat a song with.
- One could also create reverb, echo functions and use it to make it sound better :)
- Read in a .wave song and extract the frequencies using a Fourier Transform, ftt for example.
- feel free to do anything else that comes into your mind
