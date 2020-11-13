"""
This code is companion to the article "Ridge energy for thin nematic polymer networks", by
    Andrea Pedrini (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;
    Epifanio G. Virga (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.

"""

#############################
# parameters of the problem #
#############################
# weights of constraints
lambda_1 = 30
lambda_2 = 10
lambda_3 = 10
lambda_4 = 10

##################################
# parameters of the optimization #
##################################
m = 50  # number of attempts (with different random initializations)
epochs = 40
items = 500  # optimization steps in each epoch
learning_rate = 0.01
seed = 123

###################
# plots utilities #
###################

# size of figures (in inches)
fig_size = [16, 9]
