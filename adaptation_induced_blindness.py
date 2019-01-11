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

def movingGabors(fix, gab, pos, freq, refRate):
    """ Draws drifting Gabors at predefined frequency"""
    gab.setPhase(freq/refRate, '+')
    for i in range(len(pos)):
        gab.setPos(newPos = pos[i])
        gab.draw()
    fix.draw()
    experiment_window.flip()


trial_timer = core.Clock()
refRate = 60 # 1 second
# nTrials =

experiment_window = visual.Window([800,600], allowGUI=True,
    monitor='testMonitor', units='deg')

# Create TrialHandler for 16 conditions: two orientations and eight positions
targetResponses = []
targetPositions = positionGabors(degree=6)
for i in range(16):
    position = targetPositions[i%8]
    correctResponse = 'space'
    if i < 8:
        orientation = 0 # vertical
    else:
        orientation = 90 # horizontal
    targetResponses.append({'Orientation': orientation, 'Position': position,
        'CorrectResponse':correctResponse})
trials = data.TrialHandler(targetResponses, 1, method='random')

# Create stimuli
adaptor = visual.GratingStim(experiment_window, sf=1.5, size=2,
    mask='gauss', ori=0, phase= 0.5, contrast=1)
target = visual.GratingStim(experiment_window, sf=1.5, size=2,
    mask='gauss', ori=0, phase= 0.5, contrast=1) # will be modified during experiment
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

# First adaptation period (change to 30 sec)
for frameN in range(refRate):
    movingGabors(fixation, adaptor, positionGabors(degree=6), 8, refRate)

# Trials
for trial in trials:
    # Re-adaptation
    for frameN in range(refRate): # change to 5 sec
        movingGabors(fixation, adaptor, positionGabors(degree=6), 8, refRate)

    #for frameN in range(0.4*refRate): # Wait for 400ms --> explain in report
    fixation.draw()
    experiment_window.flip()
    core.wait(0.4)

    # Presentation target
    target.setPos(newPos = trial['Position'])
    target.setOri(newOri = trial['Orientation'])
    for frameN in range(2*refRate): #for exactly 120 frames i.e. 2000ms --> fix time from seconds to frame
        if frameN <= refRate: # onset 1000ms
            target.setContrast(newContrast = frameN/refRate)
        else: # offset 1000ms
            target.setContrast(newContrast = (2*refRate - frameN)/refRate)
        target.draw()
        fixation.draw()
        experiment_window.flip()

core.wait(1)

experiment_window.close()
core.quit()
