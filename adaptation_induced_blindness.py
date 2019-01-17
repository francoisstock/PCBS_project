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

def movingGabors(fix, gabors, pos, freq, rate, sec):
    """ Draws drifting Gabors at predefined frequency"""
    for frameN in range(sec*rate):
        gabors.phases += freq/rate
        gabors.draw()
        fix.draw()
        experiment_window.flip()

def contrastGabor(fix, gabor, direction, rate, sec):
    for frameN in range(sec*rate):
        if direction == 'onset':
            gabor.setContrast(newContrast = (frameN+1)/(sec*rate))
        elif direction == 'offset':
            gabor.setContrast(newContrast = (1 - (frameN+1)/(sec*rate)))
        gabor.draw()
        fix.draw()
        experiment_window.flip()


trial_timer = core.Clock()
refRate = 60
nConditions = 16 # 2 orientations and 8 positions
nTrials = 16

experiment_window = visual.Window([1366,768], allowGUI=True,
    monitor='testMonitor', units='deg')

# Create TrialHandler for 16 conditions:
targetResponses = []
targetPositions = positionGabors(degree=6)
for i in range(nConditions):
    position = targetPositions[i%8]
    correctResponse = 'space'
    if i < 8:
        orientation = 0 # vertical
    else:
        orientation = 90 # horizontal
    targetResponses.append({'Orientation': orientation, 'Position': position,
        'CorrectResponse':correctResponse})
trials = data.TrialHandler(targetResponses, nTrials/nConditions,
    method='random')

# Create stimuli
adaptors = visual.ElementArrayStim(win=experiment_window, units='deg',
    fieldPos= positionGabors(degree=6), nElements=8, sizes=2.0, sfs=1.5,
    contrs=1, phases=0.5, elementMask='gauss') # generates 8 Gabors
target = visual.GratingStim(experiment_window, sf=1.5, size=2,
    mask='gauss', ori=0, phase= 0.5, contrast=1)
fixation = visual.TextStim(experiment_window,text=('+'),
    alignHoriz="center", color = 'white')

# display instructions and wait for key press
message1 = visual.TextStim(experiment_window, pos=[0,+3],text='Hit a key when ready.')
message2 = visual.TextStim(experiment_window, pos=[0,-3],
    text='Look at the fixation cross /nPress space key when you see target')
message1.draw()
message2.draw()
fixation.draw()
experiment_window.flip()
event.waitKeys()

# First adaptation period
movingGabors(fixation, adaptors, pos = positionGabors(degree=6),
    rate=refRate, freq=8, sec=3)

# Trials
for trial in trials:
    # Re-adaptation
    movingGabors(fixation, adaptors, pos = positionGabors(degree=6),
        rate=refRate, freq=8, sec=1)

    #for frameN in range(0.4*refRate): # Wait for 400ms --> explain in report
    fixation.draw()
    experiment_window.flip()
    core.wait(0.4)

    # Target
    target.setPos(newPos = trial['Position'])
    target.setOri(newOri = trial['Orientation'])
    contrastGabor(fixation, target, direction='onset', rate=refRate, sec=1)
    contrastGabor(fixation, target, direction='offset', rate=refRate, sec=3)

core.wait(1)

experiment_window.close()
core.quit()
