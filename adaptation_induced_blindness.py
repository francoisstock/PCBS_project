"""
Adaptation-Induced-Blindness (AIB) experiment
"""

from psychopy import data, visual, core, event, gui, clock
from psychopy.tools.filetools import fromFile, toFile

from numpy import cos, sin, pi

def positionGabors(degree, n=8):
    """ Return a list with n positions on an imaginary cycle"""
    pos = []
    for i in range(0, n):
        pos.append([degree*cos(i*2*pi/n), degree*sin(i*2*pi/n)])
    return pos

def movingGabors(win, fix, gabors, freq, rate, sec):
    """ Draw drifting Gabors at given frequency"""
    for frameN in range(sec*rate):
        for i in range(len(gabors)):
            gabors[i].setPhase(freq/rate, '+')
            gabors[i].draw()
        fix.draw()
        win.flip()


# Retrieve or create a parameters file and present a dialogue box
try:
    expInfo = fromFile('lastParams.pickle')
except:
    expInfo = {'SubjectNumber':'enter number'}
expInfo['dateStr'] = data.getDateStr()  # add the current time

dlg = gui.DlgFromDict(expInfo, title='AIB Exp', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

# Text file to save data
fileName = expInfo['SubjectNumber'] + '_' + expInfo['dateStr']
dataFile = open(fileName+'.csv', 'w')
dataFile.write('positionHor,positionVer,orientation,response,rt\n')

# Some general parameters
trial_timer = core.Clock()
nConditions = 16 # 2 orientations and 8 positions
nTrials = 16
refRate = 60

# Create TrialHandler:
targetResponses = []
for i in range(nConditions):
    if i < 8:
        orientation = 0 # vertical
    else:
        orientation = 90 # horizontal
    position = positionGabors(degree=6)[i%8]
    targetResponses.append({'Orientation': orientation,
                            'Position': position})
trials = data.TrialHandler(targetResponses, nTrials/nConditions,
                           method='random')

# Create window and stimuli
experiment_window = visual.Window([1366,768], allowGUI=True,
                                  monitor='testMonitor', units='deg')

adaptors = []
for i in range(8):
    gabor = visual.GratingStim(experiment_window, sf=1.4, size=2, phase= 0.5,
                               ori=0, contrast=1, mask='gauss',
                               pos=positionGabors(degree=6)[i])
    adaptors.append(gabor)

target = visual.GratingStim(experiment_window, sf=1.4, size=2, phase=0.5,
                            ori=0, contrast=1, mask='gauss')

fixation = visual.GratingStim(experiment_window, color=-1, colorSpace='rgb',
                              tex=None, mask='circle', size=0.2)

# display instructions and wait for key press
message1 = visual.TextStim(experiment_window, pos=[0,+3],
                           text='Hit a key when ready.')
message2 = visual.TextStim(
    experiment_window, pos=[0,-4],
    text='Look at the fixation cross.\nPress space key when you see target.')
message1.draw()
message2.draw()
fixation.draw()
experiment_window.flip()
event.waitKeys()

# First adaptation period
movingGabors(experiment_window, fixation, adaptors, rate=refRate,
             freq=8, sec=20)

# Trials
for thisTrial in trials:

    # Re-adaptation
    movingGabors(experiment_window, fixation, adaptors, rate=refRate,
                 freq=8, sec=5)

    # Some useful parameters specific to each trial
    pos = thisTrial['Position']
    ori = thisTrial['Orientation']
    target.setPos(newPos =pos)
    target.setOri(newOri = ori)
    thisResp = 0
    rt = None
    timeTarget = clock.getTime()

    # Present target and record reaction
    for frameN in range(120):
        if frameN < 60:
            target.setContrast(newContrast=(frameN+1)/60) #onset
        else:
            target.setContrast(newContrast=2-(frameN+1)/60) #offset
        target.draw()
        fixation.draw()
        experiment_window.flip()

        allKeys= event.getKeys()
        for thisKey in allKeys:
            if thisKey=='space':
                 thisResp = 1
                 rt = clock.getTime() - timeTarget

    dataFile.write('{p[0]},{p[1]}'.format(p=pos))
    dataFile.write(',{},{},{}\n'.format(ori, thisResp, rt))

core.wait(1)

experiment_window.close()
core.quit()
