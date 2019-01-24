# Project: Adaptation-induced-blindness (AIB) experiment

The aim of this project was to create a psychophysics experiment implementing a task using the Adaptation-induced-blindness illusion (Motoyoshi et Hayakawa, 2010).

The experiment is separated in two parts: adaptation and target presentation. The participants must indicate using a keypress if they perceive the target. Reaction time after target presentation is recorded.

First the participants are presented with adaptors i.e. eight drifting Gabors on an imaginary circle. Second, they are then presented with the target, a single Gabor whose contrast increases gradually to maximal value and then decreases gradually again to 0. The targets are either horizontal or vertical, and the hypothesis is that only the former will be perceived (Athrop et al, 2017).

Table of Contents

 - Adaptation-induced-blindness experiment
  - Dialog box
  - General parameters
  - TrialHandler
  - Stimuli and instructions
  - Experiment
   - Useful functions
   - Recording answers
  - Conclusion
  - Bibliography
 
 Dialog box
 
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

TrialHandler

Stimuli and instructions

Experiment

Useful functions

Recording answers

Conclusion

If I had more time:
 - Analysis of the data
 Coding level and what I learned

Bibliography

Motoyoshi et Hayakawa (2010) : https://jov.arvojournals.org/article.aspx?articleid=2121085
Athrop et al (2017): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5433556/
