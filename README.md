# Project: Adaptation-induced-blindness (AIB) experiment

The aim of this project was to create a psychophysics experiment implementing a task using the Adaptation-induced-blindness illusion (Motoyoshi et Hayakawa, 2010).

The experiment is separated in two parts: a facilitation period and then target presentation. The participants must indicate using a keypress if they perceive the target. Reaction time after target presentation is recorded. PsychoPy is used to expose the stimuli.

First, the participants are presented with adaptors i.e. eight drifting Gabor patches on an imaginary circle. Second, they are presented with the target, a single Gabor patch whose contrast increases gradually to maximal value and then decreases gradually again to 0. The targets are either horizontal or vertical, and the hypothesis is that only the former will be perceived consciously (Apthorp et al, 2017).

Table of Contents

 * Adaptation-induced-blindness experiment
    * Dialog box
    * General parameters and output file
    * TrialHandler
    * Stimuli and instructions
    * Experiment
      * Facilitation
      * Target presentation
      * Recording answers and output
    * Conclusion
    * Bibliography
 
 Dialog box
 ========
 
First we try to load a parameter file if the experiment has already been run. If that fails, the code creates a default set of parameters that are stored in a dictionary called _expInfo_. The current time is then recorded in the parameter file.

try:  
    expInfo = fromFile('lastParams.pickle')  
except:  
    expInfo = {'SubjectNumber':'enter_number'}  
    
expInfo['dateStr'] = data.getDateStr()  # add the current time  

A dialog box _dlg_ is created, in which the subject number is added manually.

dlg = gui.DlgFromDict(expInfo, title='AIB Exp', fixed=['dateStr'])  
if dlg.OK:  
    toFile('lastParams.pickle', expInfo)  # save params to file for next time  
else:  
    core.quit()  # the user hit cancel so exit

General parameters and output file
=====================

A csv file is created, named using the parameters file (subject number and time of the experiment). A name is given for each column of data that will be collected. This includes the trial identity i.e. how far away from the fixation point on the x and y axes the target is and its orientation (_positionHor_, _positionVer_ and _orientation_), a Boolean including whether the space key was pressed or not (_response_) and reaction time (_rt_).

fileName = expInfo['SubjectNumber'] + '_' + expInfo['dateStr']  
dataFile = open(fileName+'.csv', 'w')  
dataFile.write('positionHor,positionVer,orientation,response,rt\n')  

Then some general parameters are defined. A clock keeps track of time during the experiment. The number of conditions is then specified: 16 for the 8 positions and 2 orientations (verical-horizontal) of the target. Then the number of trials is also determine: Here there are only 16 so that the experiment is hsort and one datum is collected to each condition. If running the experiment to get useful data, it is necessary to increase the number of trials in order to have enough data to generalise for each conditions (Careful: nTrials must be divisible by 16 for the TrialHandler to work properly). Finally, the refresh rate is set at 60Hz here, and the variable can be modified easily to adapt the experiment to the refresh rate of the device on which it is run.

trial_timer = core.Clock()  
nConditions = 16 # 2 orientations and 8 positions  
nTrials = 16  
refRate = 60  

TrialHandler
========

This class is utilised to handle trial sequencing. It allows to define the specificities (here the position of the target and its orientation) of each condition in advance of the experiment. The position of the gabors are determined using a function (_positionGabors_) that was defined at the beginning of the module and returns n equidistant Gabor patches on an imaginary circle whith a specified radius (here 6 degrees). How many trials there is for each condition is specified, and the trials are randomised in advance of running the experiment.

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
                           

Preparation of stimuli
============

List with adaptors to be used later to expose them all at the same time. The target's position is determined later on in the experiment by the TrialHandler.

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

Experiment
=====

## Facilitation

First facilitation period with presentation of adaptors drifting at 8Hz for 20 seconds. 

movingGabors(experiment_window, fixation, adaptors, rate=refRate,  
             freq=8, sec=20)  

Defined function.

def movingGabors(win, fix, gabors, freq, rate, sec):  
    """ Draw drifting Gabors at given frequency"""  
    for frameN in range(sec*rate):  
        for i in range(len(gabors)):  
            gabors[i].setPhase(freq/rate, '+')  
            gabors[i].draw()  
        fix.draw()  
        win.flip()  

## Target presentation

Second presentation of each target trial by trial. Also facilitation "top up" between trials.

for thisTrial in trials:

   movingGabors(experiment_window, fixation, adaptors, rate=refRate,
                 freq=8, sec=5)

Then some useful parameters for the specific trial are defined. Some of this information is extacted from the TrialHandler, and we create variables and set a time for recording the participants' answers

pos = thisTrial['Position']
ori = thisTrial['Orientation']
target.setPos(newPos =pos)
target.setOri(newOri = ori)
thisResp = 0
rt = None
timeTarget = clock.getTime()

The target is presented, with a gradually changing contrast with onset and offset both at 1000ms.

for frameN in range(120):  
        if frameN < 60:  
            target.setContrast(newContrast=(frameN+1)/60) #onset  
        else:  
            target.setContrast(newContrast=2-(frameN+1)/60) #offset  
        target.draw()  
        fixation.draw()  
        experiment_window.flip()  

## Recording answers and output data file

For each trial, record both keypress indicating that participant perceived the stimulus and in case he did the reaction time. Use trial-specific paramers to also record trial identity (distance from fixation on x and y axis, and horizontal or vertical position).

allKeys= event.getKeys()
        for thisKey in allKeys:
            if thisKey=='space':
                 thisResp = 1
                 rt = clock.getTime() - timeTarget

Output a csv file

dataFile.write('{p[0]},{p[1]}'.format(p=pos))  
dataFile.write(',{},{},{}\n'.format(ori, thisResp, rt))  

Conclusion
======

If I had more time:
 - Analysis of the data  
 
I would describe myself as a beginner in programming before the beginning of the class. My only experience was coding an experiment with Matlab during a five-week internship last summer. So my first experience with Python was this class. In this class I learned, among other things, the basics of the Python language and some essential functions, how to define functions in Python, how to use Expyriment and Psychopy to expose stimuli in psychophysical experiments, how to format strings and how to output a data file with the data generated during an experiment. My suggestion for the future would be to give a grade (even one that counts for a very small percentage of the final mark) for some of the simple exercises that we did at the beginning of the class. Unfortunately, I think it is harder to motivate oneself to work for a class with no short-term goals when we have many other classes running at the same time which have regular assessment.

Bibliography
========

Apthorp, D., Griffiths, S., Alais, D., & Cass., J. (2017). Adaptation-Induced blindness is orientation-tuned and monocular. _I-Perception_, 8(2), 1-15. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5433556/  
Motoyoshi, I. & Hayakawa, S. (2010).Adaptation-induced blindness to sluggish stimuli. _Journal of Vision_, 10(2), 1-8. https://jov.arvojournals.org/article.aspx?articleid=2121085  
