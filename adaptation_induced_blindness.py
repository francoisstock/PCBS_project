"""
Adaptation-Induced-Blindness (AIB) illusion

In this illusion a Gabor patch is perceived unconsciously even though it
reaches maximum contrast. Two steps:
 - Adaptation period: 8 gabor patches on a virtual circle around the fixation
cross. They are presented at a maximal contrast and flicker with a speed of
8Hz.
 - Stimulus presentation: one gabor is presented in one of the 8 positions. It
gradually reaches maximal contrast in 1000ms and then decreases to minimal
contrast in 1000ms.
More on AIB: https://www.ncbi.nlm.nih.gov/pubmed/20462317
"""

from psychopy import data, visual, core, event
import random
from numpy import cos, sin, pi

# Create TrialHandler for two conditions: vertical or horizontal target
visual_targets = [1,2] # 1 = vertical, 2 = horizontal
targets_responses = []
for target in visual_targets: # Simplify?
    correct_response = 'space'
    targets_responses.append({'Target':target, 'CorrectResponse':correct_response})
trials = data.TrialHandler(targets_responses, 2, method='random')

# Create data table
trials.data.addDataType('Response')
trials.data.addDataType('Accuracy')

#Create a window
experiment_window = visual.Window([800,600],allowGUI=True,
    monitor='testMonitor', units='deg')

#Stimuli
gabor = visual.GratingStim(experiment_window, sf=1.5, size=2,
    mask='gauss', ori=0, phase= 0.5, contrast=1)
fixation = visual.TextStim(experiment_window,text=('+'),
    alignHoriz="center", color = 'white')

# Determine the 8 positions of the target (randomly picked during the trials)
targetAngle = 0
targetDistance = 6
targetPositions = []
for i in range(0,8):
    xAngle, yAngle = cos(targetAngle), sin(targetAngle)
    targetPositions.append([targetDistance*xAngle, targetDistance*yAngle])
    targetAngle += pi/4

# Set timer
trial_timer = core.Clock()

# display instructions and wait for key press
message1 = visual.TextStim(experiment_window, pos=[0,+3],text='Hit a key when ready.')
message2 = visual.TextStim(experiment_window, pos=[0,-3],
    text='Instructions')
message1.draw()
message2.draw()
fixation.draw()
experiment_window.flip()
event.waitKeys()

# First adaptation period (change to 30 sec)
for frameN in range(200):
    fixation.draw()
    gabor.setPhase(0.05, '+')
    for eachPosition in range(8):
        gabor.setPos(newPos = targetPositions[eachPosition])
        gabor.draw()
    experiment_window.flip()

# Trials
for trial in trials:
    current_time = 0
    trial_still_running = True
    trial_timer.reset()

    # Set additional target parameters
    gabor.setPos(newPos = random.choice(targetPositions))  # Randomly pick one of the 8 positions
    gabor.setOri(newOri = 0) # Reset Ori

    # Re-adaptation (change to 5 sec)
    for frameN in range(100):
        fixation.draw()
        gabor.setPhase(0.05, '+')
        for eachPosition in range(8):
            gabor.setPos(newPos = targetPositions[eachPosition])
            gabor.draw()
        experiment_window.flip()

    for frameN in range(2000): #for exactly 120 frames i.e. 2000ms --> fix time from seconds to frame
        current_time = trial_timer.getTime()

        if frameN < 400:  # present fixation for 400ms
            fixation.draw()

        elif frameN >= 401 and frameN < 1999:
            fixation.draw()

            if trial['Target'] == 2: # Horizontal target
                gabor.setOri(newOri = 90)
            gabor.draw()

            responded = event.getKeys()
            if responded:
                if trial['CorrectResponse'] == responded[0]:
                    accuracy = 1
                    timing = current_time
            else: accuracy = 0

        elif frameN >= 1999:
            fixation.draw()
            if not responded:
                accuracy = 0

        experiment_window.flip()

experiment_window.close()
core.quit()

# Save data
