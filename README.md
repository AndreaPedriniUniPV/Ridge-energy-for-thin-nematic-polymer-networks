# Ridge energy for thin nematic polymer networks - accompanying ESI

This code is companion to the article **_"Ridge energy for thin nematic polymer networks"_**, submitted to *EPJE*.

#### Authors
*Andrea Pedrini* (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;

*Epifanio G. Virga* (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.


## Purpose

The main purpose of this code is to find a numeric approximation to the *disembodied elastica*, a  chain of articulated rods, 
which pays an elastic disalignment cost (*Ridge Energy*) at the edges.

For any further detail about the mathematical methods and for a discussion of the results, we refer the reader to the associated article. 

## Prerequisites

Use python 3.x

See also requirements.txt

## Files
The following files are included in the online repository:

* README.md   -- this readme
* run.py      -- the main file
* lib         -- folder containing:
    * config.py     -- parameters for advanced configuration
    * energy.py  -- source code for enegy computation
    * plot.py       -- source code for plots
    * varia.py      -- source code for utilities
* requirements.txt

## Test
To test that everything is properly working, execute:
```
python3 run.py
```
A default experiment will start and at the end a plot window will open.

Two new folders are created during the run:
* plots   -- contains the results of the experiment (a .svg file for the final plot)
* logs      -- contains the log file of the experiment
    
## Experiments
File run.py can be run with different parameters:

* `n`       -- geometric parameter: number of rods in the disembodied elastica (default=10)
* `a`        -- geometric parameter: ratio of total length of the elastica to distance to clamps (default=0.6)
* `plot`      -- if True: the experiment results are displayed in a plot window (default=True)
* `save`      -- if True: the experiment plots are saved (as .svg files, in the results folder) (default=True)

Example: the code
```
python3 run.py --n 10 --a 0.6 --k24 0.8 --plot True --save True
```
starts an experiment where n=10, a=0.6, the plot is displayed and saved.

#### Plot window
We give here a brief description of what is shown in the plot window.

The title contains the values of the geometric parameters `n` and `a` for the experiment.

The first plot (top left) displays the minimizer angles theta (green) and phi (orange) 
at each articulated edge where two adjacent rods concur.

The second plot (below the first one) displays the total energy values obtained at each *attempt*.
The attempts differ one from each others in the random initialization of angles theta and phi that are optimized during
the optimization process. The default number of attempts is `m = 50` (see congig.py) and the multiplicity of attempts 
is motivated by the existence of many different local minima for the problem: different initial configurations may lead
to different local minima, so that is required a variety of attempts to encounter a global minimum.

The third plot (below the third one) displays the energy values obtained at each *attempt*.

The four plots on the bottom-right display the constraints values obtained at each *attempt*.

On the top-right corner, the main 3D plot shows the configuration of the disembodied elastica with minimal energy,
associated with the minimizer angles theta and phi.

## Advanced configuration 
File config.py collects further parameters that can be used for advanced configuration of the program:
- `lambda_1`, `lambda_2`, `lambda_3`, `lambda_4` are the weights in the total e energy that ensure the geometric
constraints of the problem are fulfilled. They force, respectively, the clamps to be at a distance of `a` (`lambda_1`)
vertically aligned (`lambda_2` and `lambda_3`), while the last constraint (`lambda_4`) ensures that the angle 
theta varies between 0 and pi.
- `m` is the number of attempts (with different random initializations)
- `epochs` is the number of epochs for the optimization of each attempt
- `items` is the number of optimization steps in each epoch
- `learning_rate` is the learning rate for Adam optimizer
- `seed` is the global seed for random initialization
- `fig_size` is the size of figures (in inches)