"""
Adaptation-Induced-Blindness (AIB)
"""

from psychopy import data, visual, core, event
from numpy import cos, sin, pi

def positionGabors(degree, n=8):
    """ Returns a list with positions for n Gabors on an imaginary cycle"""
    positions = []
    for i in range(0, n):
        positions.append([degree*cos(i*2*pi/n), degree*sin(i*2*pi/n)])
    return positions

def movingGabors(win, fix, gabors, freq, rate, sec):
    """ Draws drifting Gabors at predefined frequency"""
    for frameN in range(sec*rate):
        for i in range(len(gabors)):
            gabors[i].setPhase(freq/rate, '+')
            gabors[i].draw()
        fix.draw()
        win.flip()

def contrastGabor(win, fix, gabor, direction, rate, sec):
    for frameN in range(sec*rate):
        if direction == 'onset':
            gabor.setContrast(newContrast = (frameN+1)/(sec*rate))
        elif direction == 'offset':
            gabor.setContrast(newContrast = (1 - (frameN+1)/(sec*rate)))
        gabor.draw()
        fix.draw()
        win.flip()


trial_timer = core.Clock()
refRate = 60
nConditions = 16 # 2 orientations and 8 positions
nTrials = 16

experiment_window = visual.Window([1366,768], allowGUI=True,
    monitor='testMonitor', units='deg')

# Create TrialHandler for 16 conditions:
targetResponses = []
for i in range(nConditions):
    if i < 8:
        orientation = 0 # vertical
    else:
        orientation = 90 # horizontal
    positionNumber = positionGabors(degree=6)[i%8]
    correctResponse = 'space'
    targetResponses.append({'Orientation': orientation,
        'Position': positionNumber, 'CorrectResponse':correctResponse})
trials = data.TrialHandler(targetResponses, nTrials/nConditions,
    method='random')

# Create stimuli
gabor = visual.GratingStim(experiment_window, sf=1.4, size=2,
    mask='gauss', ori=0, phase= 0.5, contrast=1)
adaptors = []
for i in range(8):
    adaptor = visual.GratingStim(experiment_window, sf=1.4, size=2,mask='gauss',
        ori=0, phase= 0.5, contrast=1, pos = positionGabors(degree=6)[i])
    adaptors.append(adaptor)
fixation = visual.TextStim(experiment_window,text=('+'),
    alignHoriz="center", color = 'white')

# display instructions and wait for key press
message1 = visual.TextStim(experiment_window, pos=[0,+3],text='Hit a key when ready.')
message2 = visual.TextStim(experiment_window, pos=[0,-3],
    text='Look at the fixation cross Press space key when you see target')
message1.draw()
message2.draw()
fixation.draw()
experiment_window.flip()
event.waitKeys()

# First adaptation period
movingGabors(experiment_window, fixation, adaptors, rate=refRate,
    freq=8, sec=20)

# Trials
for trial in trials:
    # Re-adaptation
    movingGabors(experiment_window, fixation, adaptors, rate=refRate,
        freq=8, sec=5)

    # Target
    gabor.setPos(newPos = trial['Position'])
    gabor.setOri(newOri = trial['Orientation'])
    contrastGabor(experiment_window,fixation, gabor, direction='onset',
        rate=refRate, sec=1)
    contrastGabor(experiment_window, fixation, gabor, direction='offset',
        rate=refRate, sec=1)

core.wait(1)

experiment_window.close()
core.quit()
