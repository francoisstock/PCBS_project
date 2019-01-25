# Project: Adaptation-induced-blindness (AIB) experiment

The aim of this project was to create a psychophysics experiment implementing a task using the Adaptation-induced-blindness illusion (Motoyoshi et Hayakawa, 2010).

The experiment is separated in two parts: adaptation and target presentation. The participants must indicate using a keypress if they perceive the target. Reaction time after target presentation is recorded. Psychopy is used to expose the stimuli.

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

Refresh rate, number conditions and number trial. Set a clock --> used later.

TrialHandler
========

Useful to deal with all the conditions. Randomisation.

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
 Coding level and what I learned

Bibliography
========

Apthorp, D., Griffiths, S., Alais, D., & Cass., J. (2017). Adaptation-Induced blindness is orientation-tuned and monocular. _I-Perception_, 8(2), 1-15. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5433556/  
Motoyoshi, I. & Hayakawa, S. (2010).Adaptation-induced blindness to sluggish stimuli. _Journal of Vision_, 10(2), 1-8. https://jov.arvojournals.org/article.aspx?articleid=2121085  
