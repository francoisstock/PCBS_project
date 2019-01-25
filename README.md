# Project: Adaptation-induced-blindness (AIB) experiment

The aim of this project was to create a psychophysics experiment implementing a task using the Adaptation-induced-blindness illusion (Motoyoshi et Hayakawa, 2010).

The experiment is separated in two parts: a facilitation period and then target presentation. The participants must indicate using a keypress if they perceive the target. Reaction time after target presentation is recorded. PsychoPy is used to expose the stimuli.

First, the participants are presented with adaptors i.e. eight drifting Gabor patches on an imaginary circle. Second, they are presented with the target, a single Gabor patch whose contrast increases gradually to maximal value and then decreases gradually again to 0. The targets are either horizontal or vertical, and the hypothesis is that only the former will be perceived consciously (Apthorp et al, 2017).

Table of Contents

 * [Adaptation-induced-blindness experiment] 
    * [Dialog box] (## Dialog box)
    * [General parameters and output file]
    * [TrialHandler]
    * [Stimuli and instructions]
    * [Experiment]
      * [Facilitation]
      * [Target presentation]
      * [Recording answers and output]
    * [Conclusion]
    * [Bibliography]
 
## Dialog box
 
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

## General parameters and output file

A csv file is created, named using the parameters file (subject number and time of the experiment). A name is given for each column of data that will be collected. This includes the trial identity i.e. how far away from the fixation point on the x and y axes the target is and its orientation (_positionHor_, _positionVer_ and _orientation_), a Boolean including whether the space key was pressed or not (_response_) and reaction time (_rt_).

fileName = expInfo['SubjectNumber'] + '_' + expInfo['dateStr']  
dataFile = open(fileName+'.csv', 'w')  
dataFile.write('positionHor,positionVer,orientation,response,rt\n')  

Then some general parameters are defined. A clock keeps track of time during the experiment. The number of conditions is then specified: 16 for the 8 positions and 2 orientations (verical-horizontal) of the target.  
The number of trials is also determined: Here there are only 16 trials so that running the experiment only takes one or two minutes. It would be necessary to increase the number of trials in order to have enough data to generalise for each condition (Careful: nTrials must be divisible by nConditions for the TrialHandler to work properly).  
Finally, the refresh rate is set at 60Hz. The variable _refRate_ can be modified easily to adapt the experiment to the refresh rate of the device on which it is run.

trial_timer = core.Clock()  
nConditions = 16 # 2 orientations and 8 positions  
nTrials = 16  
refRate = 60  

TrialHandler
========

This class is used to handle trial sequencing. It allows to define the specificities (here the position of the target and its orientation) of each condition before running the experiment. The position of the gabors are determined using a function (_positionGabors_) defined at the beginning of the module, which returns n equidistant Gabor patches on an imaginary circle whith a specified radius (here 6 degrees). The number of trials for each condition is specified (_nTrials/nConditions_), and the order of the trials is randomised.

targetResponses = []  
for i in range(nConditions):  
    if i < 8:  
        orientation = 0 # vertical  
    else:  
        orientation = 90 # horizontal  
    position = positionGabors(radius=6)[i%8]  
    targetResponses.append({'Orientation': orientation,  
                            'Position': position})  
trials = data.TrialHandler(targetResponses, nTrials/nConditions,  
                           method='random')  
                           

Preparation of stimuli
============

After having called an experimental window, the stimuli are created. First, a list with the eight adaptors is created, in which the Gabor patches only differ by their position (defined by _positionGabors_). Second, another Gabor which will be used as target is created. Its position is not specified yet, as it will be change from trial to trial (the position for each trial is  determined by the TrialHandler).

adaptors = []  
for i in range(8):  
    gabor = visual.GratingStim(experiment_window, sf=1.4, size=2, phase= 0.5,  
                               ori=0, contrast=1, mask='gauss',  
                               pos=positionGabors(radius=6)[i])  
    adaptors.append(gabor)  

target = visual.GratingStim(experiment_window, sf=1.4, size=2, phase=0.5,  
                            ori=0, contrast=1, mask='gauss')  

Experiment
=====

## Facilitation

The experiment starts with a 20 seconds long facilitation period. The function _movingGabor_, defined at the beginning, of the module, is called. This function manipulates the Gabor patches in the adaptors list by changing their phase on each frame, so that when they are drawn they drift at a rate of 8Hz. 

movingGabors(experiment_window, fixation, adaptors, rate=refRate,  
             freq=8, sec=20)  

def movingGabors(win, fix, gabors, freq, rate, sec):  
    """ Draw drifting Gabors at given frequency"""  
    for frameN in range(sec*rate):  
        for i in range(len(gabors)):  
            gabors[i].setPhase(freq/rate, '+')  
            gabors[i].draw()  
        fix.draw()  
        win.flip()  

## Target presentation

A _for loop_ is initiated for trial presentation. The trial starts with a new round of 5 seconds of facilitation to make sure participants are still adapted.

for thisTrial in trials:

   movingGabors(experiment_window, fixation, adaptors, rate=refRate,
                 freq=8, sec=5)

Then some useful parameters specific to the trial are extracted from the TrialHandler. In order to record the participants' answers, some variables are defined and we record the time just before presenting the target.

   pos = thisTrial['Position']
   ori = thisTrial['Orientation']
   target.setPos(newPos =pos)
   target.setOri(newOri = ori)
   thisResp = 0
   rt = None
   timeTarget = clock.getTime()

The target is then presented. It starts with contrast 0 and then the contrast gradually increases to 1 during 1000ms. It then decreases gradually back to 0 for 1000ms too.

   for frameN in range(refRate*2):  
        if frameN < refRate:  
            target.setContrast(newContrast=(frameN+1)/refRate) #onset  
        else:  
            target.setContrast(newContrast=2-(frameN+1)/refRate) #offset  
        target.draw()  
        fixation.draw()  
        experiment_window.flip()  

## Recording answers and output data file

For each trial, the variable _thisKey_ records whether the participant pressed the 'space' key, indicating that they have perceived the target. If no keypress is recorded, the variable remains equal to 0. The time when the key is pressed is obtained, and the time when the trial started is substracted from it in order to determine the reaction time.

allKeys= event.getKeys()
        for thisKey in allKeys:
            if thisKey=='space':
                 thisResp = 1
                 rt = clock.getTime() - timeTarget

The results are written in a csv file, in which the trial identity (distance from fixation on x and y axis and orientation) is also recorded.

dataFile.write('{p[0]},{p[1]}'.format(p=pos))  
dataFile.write(',{},{},{}\n'.format(ori, thisResp, rt))  

Conclusion
======

What I would have done if I had more time to work on this project:
 - Run the experiment with a higher nTrials in order to collect some useful data.  
 - Analyse the data thus generated in order to determine whether there is indeed a difference between vertical and horizontal stimuli.  
 
I conclude this report with some words about my programming experience and what I learned during this class. I was a beginner before the start of the class. My only predious experience was coding an experiment with Matlab during a five-week internship last summer. So my first experience with Python was for this class.  
In this class I learned, among other things, the basics of the Python language and how to use some of its most important modules and functions, how to define functions in Python, how to use Expyriment and Psychopy to expose stimuli in psychophysical experiments, how to format strings and how to output a data file with the data generated during an experiment.  
My suggestion for the future would be to give a grade (even one that counts for a very small percentage of the final mark) for some of the simple exercises that we did at the beginning of the class. Unfortunately, I think it is harder to motivate oneself to work for a class with no short-term goals when we have many other classes running at the same time which have regular assessment.

Bibliography
========

Apthorp, D., Griffiths, S., Alais, D., & Cass., J. (2017). Adaptation-Induced blindness is orientation-tuned and monocular. _I-Perception_, 8(2), 1-15. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5433556/  
Motoyoshi, I. & Hayakawa, S. (2010).Adaptation-induced blindness to sluggish stimuli. _Journal of Vision_, 10(2), 1-8. https://jov.arvojournals.org/article.aspx?articleid=2121085  
