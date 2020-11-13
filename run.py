"""
This code is companion to the article "Ridge energy for thin nematic polymer networks", by
    Andrea Pedrini (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;
    Epifanio G. Virga (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.
"""

import os
import sys
import argparse
import warnings

from lib.energy import optimize_energy
from lib.varia import experiment_name, stream_tee, safe_mkdir

# Using GPU may result in a slower execution on some hardware...
# os.environ["CUDA_VISIBLE_DEVICES"] = '-1'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
warnings.simplefilter("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--n', type=float,
                    default=10,
                    help='Number of segments')
parser.add_argument('--a', type=float,
                    default=0.6,
                    help='Ratio of distance between clamps to total length of elastica')
parser.add_argument('--plot', type=bool,
                    default=True,
                    help='Plot experiment results')
parser.add_argument('--save', type=bool,
                    default=True,
                    help='Save experiment plot')
FLAGS, _ = parser.parse_known_args()

# parameters
n_val = FLAGS.n
a_val = FLAGS.a

run_name = experiment_name(n_val, a_val)

safe_mkdir('logs')
logfile = open(os.path.join('logs', '{0}.txt'.format(run_name)), 'w+')
sys.stdout = stream_tee(sys.stdout, logfile)

if FLAGS.save:
    safe_mkdir('plots')

# perform optimization
optimize_energy(n=n_val, a=a_val, run_name=run_name, save_plots=FLAGS.save, plot_show=FLAGS.plot,
                plot_home='plots')

logfile.close()
