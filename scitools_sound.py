# taken from http://hplgit.github.io/scitools/doc/api/html/_modules/scitools/sound.html

import math, numpy, wave, commands, sys, os

#EVC commands is out of python3  see for example
# https://stackoverflow.com/questions/11344557/replacement-for-getstatusoutput-in-python-3#11346017

max_amplitude = 2**15-1 # iinfo('int16').max if numpy >= 1.0.3


def write(data, filename, channels=1, sample_width=2, sample_rate=44100):
    """
    Writes the array data to the specified file.
    The array data type can be arbitrary as it will be
    converted to numpy.int16 in this function.
    """
    ofile = wave.open(filename, 'w')
    ofile.setnchannels(channels)
    ofile.setsampwidth(sample_width)
    ofile.setframerate(sample_rate)
    ofile.writeframesraw(data.astype(numpy.int16).tostring())
    ofile.close()

def read(filename):
    """
    Read sound data in a file and return the data as an array
    with data type numpy.int16.
    """
    ifile = wave.open(filename)
    channels = ifile.getnchannels()
    sample_width = ifile.getsampwidth()
    sample_rate = ifile.getframerate()
    frames = ifile.getnframes()
    data = ifile.readframes(frames)
    data = numpy.fromstring(data, dtype=numpy.uint16)
    return data.astype(numpy.int16)

def play(soundfile, player=None):
    """
    Play a file with name soundfile or an array soundfile.
    (The array is first written to file using the write function
    so the data type can be arbitrary.)
    The player is chosen by the programs 'open' on Mac and 'start'
    on Windows. On Linux, try different open programs for various
    distributions. If keyword argument 'player' is given, only this spesific
    commands is run.
    """
    tmpfile = 'tmp.wav'
    if isinstance(soundfile, numpy.ndarray):
        write(soundfile, tmpfile)
    elif isinstance(soundfile, str):
        tmpfile = soundfile

    if player:
        msg = 'Unable to open sound file with %s' %player
        if sys.platform[:3] == 'win':
            status = os.system('%s %s' %(player, tmpfile))
        else:
            status, output = commands.getstatusoutput('%s %s' %(player, tmpfile))
            msg += '\nError message:\n%s' %output
        if status != 0:
            raise OSError(msg)
        return

    if sys.platform[:5] == 'linux':
        open_commands = ['gnome-open', 'kmfclient exec', 'exo-open', 'xdg-open', 'open']
        for cmd in open_commands:
            status, output = commands.getstatusoutput('%s %s' %(cmd, tmpfile))
            if status == 0:
                break
        if status != 0:
            raise OSError('Unable to open sound file, try to set player'\
                              ' keyword argument.')

    elif sys.platform == 'darwin':
        commands.getstatusoutput('open %s' %tmpfile)
    else:
        # assume windows
        os.system('start %s' %tmpfile)


def note(frequency, length, amplitude=1, sample_rate=44100):
    """
    Generate the sound of a note as an array if float elements.
    """
    time_points = numpy.linspace(0, length, length*sample_rate)
    data = numpy.sin(2*numpy.pi*frequency*time_points)
    data = amplitude*data
    return data


def add_echo(data, beta=0.8, delay=0.1, sample_rate=44100):
    newdata = data.copy()
    shift = int(delay*sample_rate)  # b (math symbol)
    newdata[shift:] = beta*data[shift:] + \
                      (1-beta)*data[:len(data)-shift]
    #for i in xrange(shift, len(data)):
    #    newdata[i] = beta*data[i] + (1-beta)*data[i-shift]
    return newdata

def _test1():
    filename = 'tmp.wav'

    tone1 = max_amplitude*note(440, 1, 0.2)
    tone2 = max_amplitude*note(293.66, 1, 1)
    tone3 = max_amplitude*note(440, 1, 0.8)
    data = numpy.concatenate((tone1, tone2, tone3))
    write(data, filename)
    data = read(filename)
    play(filename)


def Nothing_Else_Matters(echo=False):
    E1 = note(164.81, .5)
    G = note(392, .5)
    B = note(493.88, .5)
    E2 = note(659.26, .5)
    intro = numpy.concatenate((E1, G, B, E2, B, G))
    high1_long = note(987.77, 1)
    high1_short = note(987.77, .5)
    high2 = note(1046.50, .5)
    high3 = note(880, .5)
    high4_long = note(659.26, 1)
    high4_medium = note(659.26, .5)
    high4_short = note(659.26, .25)
    high5 = note(739.99, .25)
    pause_long =  note(0, .5)
    pause_short = note(0, .25)
    song = numpy.concatenate(
      (intro, intro, high1_long, pause_long, high1_long,
       pause_long, pause_long,
       high1_short, high2, high1_short, high3, high1_short,
       high3, high4_short, pause_short, high4_long, pause_short,
       high4_medium, high5, high4_short))
    song *= max_amplitude
    if echo:
        song = add_echo(song, 0.6)
    return song

# equal-tempered scale:

note2freq = {
 'A#0': 29.14,
 'A#1': 58.27,
 'A#2': 116.54,
 'A#3': 233.08,
 'A#4': 466.16,
 'A#5': 932.33,
 'A#6': 1864.66,
 'A#7': 3729.31,
 'A0': 27.5,
 'A1': 55,
 'A2': 110,
 'A3': 220,
 'A4': 440,
 'A5': 880,
 'A6': 1760,
 'A7': 3520,
 'Ab0': 25.96,
 'Ab1': 51.91,
 'Ab2': 103.83,
 'Ab3': 207.65,
 'Ab4': 415.3,
 'Ab5': 830.61,
 'Ab6': 1661.22,
 'Ab7': 3322.44,
 'B0': 30.87,
 'B1': 61.74,
 'B2': 123.47,
 'B3': 246.94,
 'B4': 493.88,
 'B5': 987.77,
 'B6': 1975.53,
 'B7': 3951.07,
 'Bb0': 29.14,
 'Bb1': 58.27,
 'Bb2': 116.54,
 'Bb3': 233.08,
 'Bb4': 466.16,
 'Bb5': 932.33,
 'Bb6': 1864.66,
 'Bb7': 3729.31,
 'C#0': 17.32,
 'C#1': 34.65,
 'C#2': 69.3,
 'C#3': 138.59,
 'C#4': 277.18,
 'C#5': 554.37,
 'C#6': 1108.73,
 'C#7': 2217.46,
 'C#8': 4434.92,
 'C1': 32.7,
 'C2': 65.41,
 'C3': 130.81,
 'C4': 261.63,
 'C5': 523.25,
 'C6': 1046.5,
 'C7': 2093,
 'C8': 4186.01,
 'D#0': 19.45,
 'D#1': 38.89,
 'D#2': 77.78,
 'D#3': 155.56,
 'D#4': 311.13,
 'D#5': 622.25,
 'D#6': 1244.51,
 'D#7': 2489.02,
 'D#8': 4978.03,
 'D0': 18.35,
 'D1': 36.71,
 'D2': 73.42,
 'D3': 146.83,
 'D4': 293.66,
 'D5': 587.33,
 'D6': 1174.66,
 'D7': 2349.32,
 'D8': 4698.64,
 'Db0': 17.32,
 'Db1': 34.65,
 'Db2': 69.3,
 'Db3': 138.59,
 'Db4': 277.18,
 'Db5': 554.37,
 'Db6': 1108.73,
 'Db7': 2217.46,
 'Db8': 4434.92,
 'E0': 20.6,
 'E1': 41.2,
 'E2': 82.41,
 'E3': 164.81,
 'E4': 329.63,
 'E5': 659.26,
 'E6': 1318.51,
 'E7': 2637.02,
 'Eb0': 19.45,
 'Eb1': 38.89,
 'Eb2': 77.78,
 'Eb3': 155.56,
 'Eb4': 311.13,
 'Eb5': 622.25,
 'Eb6': 1244.51,
 'Eb7': 2489.02,
 'Eb8': 4978.03,
 'F#0': 23.12,
 'F#1': 46.25,
 'F#2': 92.5,
 'F#3': 185,
 'F#4': 369.99,
 'F#5': 739.99,
 'F#6': 1479.98,
 'F#7': 2959.96,
 'F0': 21.83,
 'F1': 43.65,
 'F2': 87.31,
 'F3': 174.61,
 'F4': 349.23,
 'F5': 698.46,
 'F6': 1396.91,
 'F7': 2793.83,
 'G#0': 25.96,
 'G#1': 51.91,
 'G#2': 103.83,
 'G#3': 207.65,
 'G#4': 415.3,
 'G#5': 830.61,
 'G#6': 1661.22,
 'G#7': 3322.44,
 'G0': 24.5,
 'G1': 49,
 'G2': 98,
 'G3': 196,
 'G4': 392,
 'G5': 783.99,
 'G6': 1567.98,
 'G7': 3135.96,
 'Gb0': 23.12,
 'Gb1': 46.25,
 'Gb2': 92.5,
 'Gb3': 185,
 'Gb4': 369.99,
 'Gb5': 739.99,
 'Gb6': 1479.98,
 'Gb7': 2959.96}
    
if __name__ == '__main__':
    #_test1()
    song = Nothing_Else_Matters(False)
    play(song)
