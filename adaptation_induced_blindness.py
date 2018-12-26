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

import expyriment
import random
import numpy as np
import math

NTRIALS = 4
ITI = 500  # inter trial interval

## Initialization
exp = expyriment.design.Experiment(name="Adaptation-Induced-Blindness")
# Set develop mode. Comment for real experiment
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)

## Creating the stimuli and trials
# Determine the parameters of the Gabor (1 degree of visual angle = 1cm if the participant is 57.3cm away from the screen)
cm_to_pix = 20 #Find pixels/cm value
distance_Gabors = 6*cm_to_pix
size_Gabors = 2*cm_to_pix

# Determine Gabor's positions
angle_Gabor = 0
for i in 8:
    x_angle, y_angle = np.cos(math.radian(angle_Gabor)), np.sin(math.radian(angle_Gabor))
    posGabor(i) = (distance_Gabors*x_angle, distance_Gabors*x_angle)
    angle_Gabor = angle_Gabor + i*45

# Make stimuli
block = expyriment.design.Block(name="Block 1")

fixcross = expyriment.stimuli.FixCross()
fixcross.preload()
rect1 = expyriment.stimuli.Rectangle((50,50), position = (200, 0)) #Replace by Gabor Patch
rect2 = expyriment.stimuli.Rectangle((50,50), position = (-200, 0))
stim1, stim2 = expyriment.stimuli.BlankScreen(), expyriment.stimuli.BlankScreen()
fixcross.plot(stim1)
rect1.plot(stim1)
stim1.preload()
fixcross.plot(stim2)
rect2.plot(stim2)
stim2.preload()

instructions = expyriment.stimuli.TextScreen("Instructions", "Always look at the fixation cross; Between each trial you will have a period of adaptation ; When the adaptators disappear, press the 'y' key as quickly as possible if you see the target and the 'n' key if you didn't see it")

for i in range(NTRIALS):
    trial = expyriment.design.Trial()
    trial.add_stimulus(fixcross)
    if random.choice((1, 2)) == 1:
        trial.add_stimulus(stim1)
    else:
        trial.add_stimulus(stim2)
    block.add_trial(trial, random_position=True)

exp.add_block(block)

kb = exp.keyboard  # response device
#exp.data_variable_names(['key', 'rt'])

## Run the experiment
expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        exp.clock.wait(ITI)
        #trial.stimuli[0].plot(trial.stimuli[1])
        trial.stimuli[0].present()
        trial.stimuli[1].present()
        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_SPACE])
        exp.data.add([block.name, trial.id, key, rt])
        #key, rt =kb.wait(keys='s', duration=2000)


expyriment.control.end()
#        trial.stimuli[0].present()
