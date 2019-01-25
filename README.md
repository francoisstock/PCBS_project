# Project: Adaptation-induced-blindness (AIB) experiment

The aim of this project was to create a psychophysics experiment implementing a task using the Adaptation-induced-blindness illusion (Motoyoshi et Hayakawa, 2010).

The experiment is separated in two parts: adaptation and target presentation. The participants must indicate using a keypress if they perceive the target. Reaction time after target presentation is recorded. PsychoPy is used to expose the stimuli.

First the participants are presented with adaptors i.e. eight drifting Gabors on an imaginary circle. Second, they are then presented with the target, a single Gabor whose contrast increases gradually to maximal value and then decreases gradually again to 0. The targets are either horizontal or vertical, and the hypothesis is that only the former will be perceived (Apthorp et al, 2017).

Table of Contents

 - Adaptation-induced-blindness experiment
    - Dialog box
    - General parameters
    - TrialHandler
    - Stimuli and instructions
    - Experiment
      - Recording answers
    - Conclusion
    - Bibliography
 
 Dialog box
 ========
 
The first lines try to load a parameter file from a previous run of the experiment, and if it fails creates a default set of parameters that are stored in a dictionary called _expInfo_.

try:  
    expInfo = fromFile('lastParams.pickle')  
except:  
    expInfo = {'SubjectNumber':'enter number'}  
expInfo['dateStr'] = data.getDateStr()  # add the current time

Then a dialog box _dlg_ is created, in which the subject number is manually added. With the current time, this data is used to name the csv file created to save the data.

dlg = gui.DlgFromDict(expInfo, title='AIB Exp', fixed=['dateStr'])  
if dlg.OK:  
    toFile('lastParams.pickle', expInfo)  # save params to file for next time  
else:  
    core.quit()  # the user hit cancel so exit

General parameters
=====================

Before starting the experiment, some general parameters are defined. A clock is defined to keep track of time during the experiment. The number of conditions is also specified: 16 for the 8 positions and 2 orientations (verical-horizontal) of the target. Then the number of trials is then determine: Here there are only 16 so that the experiment is hsort and one datum is collected to each condition. If running the experiment to get useful data, it is necessary to increase the number of trials in order to have enough data to generalise for each conditions (Careful: nTrials must be divisible by 16 for the TrialHandler to work properly). Finally, the refresh rate is set at 60Hz here, and the variable can be modified easily to adapt the experiment to the refresh rate of the device on which it is run.

trial_timer = core.Clock()  
nConditions = 16 # 2 orientations and 8 positions  
nTrials = 16  
refRate = 60  

TrialHandler
========

This class is utilised to handle trial sequencing. It allows to define the specificities (here the position of the target and its orientation) of each condition in advance of the experiment. How many trials there is for each condition is specified, and the trials are randomised in advance of running the experiment.

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
Call to function determined for positions of Gabor.

Experiment
=====

First facilitation period with presentation of adaptors drifting at 8Hz for 20 seconds. Defined function.
Second presentation of each target trial by trial. Also facilitation "top up" between trials.

## Recording answers

Record both keypress indicating that participant perceived the stimulus and in case he did the reaction time. Use trial-specific paramers to also record trial identity (distance from fixation on x and y axis, and horizontal or vertical position).
Output a csv file

Conclusion
======

If I had more time:
 - Analysis of the data  
 
I would describe myself as a beginner in programming before the beginning of the class. My only experience was coding an experiment with Matlab during a five-week internship last summer. So my first experience with Python was this class. In this class I learned, among other things, the basics of the Python language and some essential functions, how to define functions in Python, how to use Expyriment and Psychopy to expose stimuli in psychophysical experiments, how to format strings and how to output a data file with the data generated during an experiment. My suggestion for the future would be to give a grade (even one that counts for a very small percentage of the final mark) for some of the simple exercises that we did at the beginning of the class. Unfortunately, I think it is harder to motivate oneself to work for a class with no short-term goals when we have many other classes running at the same time which have regular assessment.

Bibliography
========

Apthorp, D., Griffiths, S., Alais, D., & Cass., J. (2017). Adaptation-Induced blindness is orientation-tuned and monocular. _I-Perception_, 8(2), 1-15. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5433556/  
Motoyoshi, I. & Hayakawa, S. (2010).Adaptation-induced blindness to sluggish stimuli. _Journal of Vision_, 10(2), 1-8. https://jov.arvojournals.org/article.aspx?articleid=2121085  
