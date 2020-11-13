"""
This code is a companion to the article "Ridge energy for thin nematic polymer networks", by
    Andrea Pedrini (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;
    Epifanio G. Virga (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.
"""

import os
import sys

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import lib.config as c
import lib.plot as p
import csv


def energy(theta_short, phi_short, n, a, lambda_1=c.lambda_1, lambda_2=c.lambda_2, lambda_3=c.lambda_3,
           lambda_4=c.lambda_4):
    """
    Compute the energy of rod configuration as:
    Total Energy = Ridge Energy + weighted constraints (lambda_1 * constr_1 + lambda_2 * constr_2 + lambda_3 * constr_3
        lambda_4 * constr_4)

    Input
      theta_short: a tf vector
      phi_short: a tf vector
      n: an integer
      a: a float
      lambda_1: a float
      lambda_2: a float
      lambda_3: a float
      lambda_4: a float
    """
    # clamped elastica: first and last segments are vertical (parallel to z-axis)
    # theta[0] and theta[n-1] are 0
    # phi[0] and phi[n-1] are conventionally set to 0
    # second segment is supposed to lie in yz-plane
    # phi[1] is set to 0
    theta = tf.concat([tf.constant([0], dtype=tf.float64), theta_short, tf.constant([0], dtype=tf.float64)], 0)
    phi = tf.concat([tf.constant([0], dtype=tf.float64), tf.constant([0], dtype=tf.float64), phi_short,
                     tf.constant([0], dtype=tf.float64)], 0)
    cos_theta = tf.cos(theta)
    sin_theta = tf.sin(theta)
    cos_phi = tf.cos(phi)
    sin_phi = tf.sin(phi)
    theta_shift = tf.roll(theta, shift=-1, axis=0)
    phi_shift = tf.roll(phi, shift=-1, axis=0)
    cos_theta_shift = tf.cos(theta_shift)
    sin_theta_shift = tf.sin(theta_shift)
    cos_phi_diff = tf.cos(phi_shift - phi)
    prod_1 = sin_theta_shift * sin_theta * cos_phi_diff
    prod_2 = cos_theta_shift * cos_theta
    prod_3 = sin_theta * sin_phi
    prod_4 = sin_theta * cos_phi
    sum = tf.add(prod_1, prod_2)
    arccos = tf.acos(sum)
    # ridge energy
    ridge_energy = tf.reduce_sum((arccos[:-1]) ** 2, 0)
    # force the clamps to have distance 'a' on z axis
    constr_1 = tf.abs(tf.reduce_sum(cos_theta, 0) / n - a)
    # force the clamps to have distance 0 on x axis
    constr_2 = tf.abs(tf.reduce_sum(prod_3, 0))
    # force the clamps to have distance 0 on y axis
    constr_3 = tf.abs(tf.reduce_sum(prod_4, 0))
    # force the angles theta to be in [0, pi]
    constr_4 = tf.reduce_sum(tf.nn.relu(theta * (theta - np.pi)))
    # compute total energy
    total_energy = ridge_energy + lambda_1 * constr_1 + lambda_2 * constr_2 + lambda_3 * constr_3 + lambda_4 * constr_4

    return total_energy, ridge_energy, constr_1, constr_2, constr_3, constr_4


def grad(theta_short, phi_short, n, a):
    """
    Create gradients

    Input
      theta_short: a tf vector
      phi_short: a tf vector
      n: an integer
      a: a float
    """
    with tf.GradientTape() as tape:
        total_energy, _, _, _, _, _ = energy(theta_short, phi_short, n, a)
    return tape.gradient(total_energy, [theta_short, phi_short])


def optimize_energy(n, a, run_name, m=c.m, epochs=c.epochs, items=c.items, seed=c.seed, save_plots=False,
                    plot_show=True, plot_home=''):
    """
    For each `attempt` (with random uniform generation of variables),
    the optimization process is performed by Adam Optimizer,
    for a given number of `epochs` and a given number of `items` in each epoch.
    A history of best results for each attempt is collected.

    Input
      n: an integer
      a: a float
      run_name: a string
      m: an integer
      epochs: an integer
      items: an integer
      seed: an integer
      save_results: a boolean
      plot_show: a boolean
      results_home: a string
    """

    # do not shrink printouts
    np.set_printoptions(threshold=sys.maxsize)

    print()
    print("---PARAMETERS---")
    print()
    print("n = {}".format(n))
    print("a = {}".format(a))
    print("lambda_1 = {}".format(c.lambda_1))
    print("lambda_2 = {}".format(c.lambda_2))
    print("lambda_3 = {}".format(c.lambda_3))
    print("lambda_3 = {}".format(c.lambda_4))
    print()
    print("m = {}".format(m))
    print("epochs = {}".format(epochs))
    print("items = {}".format(items))
    print("learning_rate = {}".format(c.learning_rate))
    print("seed = {}".format(c.seed))
    print()
    print()
    print("---OPTIMIZATION--")
    print()

    # ensure reproducibility of random generations:
    rng = tf.random.Generator.from_seed(seed)
    tf.random.set_global_generator(rng)

    # create empty histories
    total_energy_history = list()
    ridge_energy_history = list()
    constr_1_history = list()
    constr_2_history = list()
    constr_3_history = list()
    constr_4_history = list()
    theta_short_history = list()
    phi_short_history = list()

    # optimize each attempt
    for j in range(m):
        # create variables
        theta_short = tf.Variable(rng.uniform([n - 2], 0., np.pi, dtype=tf.float64))
        phi_short = tf.Variable(rng.uniform([n - 3], 0., 2 * np.pi, dtype=tf.float64))
        # initialize attempt
        theta_short_attempt = theta_short
        phi_short_attempt = phi_short
        total_energy_attempt, _, _, _, _, _ = energy(theta_short, phi_short, n=n, a=a)
        # optimize each epoch
        for epoch in range(epochs):
            optimizer = tf.optimizers.Adam(c.learning_rate)
            for item in range(items):
                gradients = grad(theta_short, phi_short, n=n, a=a)
                if not np.isnan(gradients[0].numpy()).any():
                    optimizer.apply_gradients(zip(gradients, [theta_short, phi_short]))
                    if epoch > 1:
                        total_energy, _, _, _, _, _ = energy(theta_short, phi_short, n=n, a=a)
                        # update best angles theta and phi
                        if total_energy < total_energy_attempt:
                            total_energy_attempt = total_energy
                            theta_short_attempt = theta_short
                            phi_short_attempt = phi_short
        # update histories attempt
        theta_short_history.append(theta_short_attempt)
        phi_short_history.append(phi_short_attempt)
        total_energy, ridge_energy, constr_1, constr_2, constr_3, constr_4 = energy(theta_short_attempt,
                                                                                    phi_short_attempt, n=n, a=a)
        total_energy_history.append(total_energy)
        ridge_energy_history.append(ridge_energy)
        constr_1_history.append(constr_1)
        constr_2_history.append(constr_2)
        constr_3_history.append(constr_3)
        constr_4_history.append(constr_4)
        print(
            "Attempt: {} - total_energy: {} - ridge_energy: {} - constraint_1: {} - constraint_2: {} - constraint_3: {} - constraint_4: {}".format(
                j, total_energy, ridge_energy, constr_1, constr_2, constr_3, constr_4))

    # Display result

    m_best = int(np.argmin(total_energy_history))

    # Print best angles
    theta = tf.concat(
        [tf.constant([0], dtype=tf.float64), theta_short_history[m_best], tf.constant([0], dtype=tf.float64)],
        0)
    phi = tf.concat([tf.constant([0], dtype=tf.float64), tf.constant([0], dtype=tf.float64), phi_short_history[m_best],
                     tf.constant([0], dtype=tf.float64)], 0)
    print()
    print()
    print("---RESULTS---")
    print()
    print("Best theta: {}".format(theta.numpy()))
    print("and best phi: {}".format(phi.numpy()))
    print("with Ridge Energy: {}".format(ridge_energy_history[m_best]))
    print("found at epoch: {}".format(m_best))

    # Print tangent vectors
    t_x_list = np.sin(theta.numpy()) * np.cos(phi.numpy())
    t_y_list = np.sin(theta.numpy()) * np.sin(phi.numpy())
    t_z_list = np.cos(theta.numpy())
    print()
    print("Tangent vectors")
    print("t_x_list: {} ".format(t_x_list))
    print("t_y_list: {} ".format(t_y_list))
    print("t_z_list: {} ".format(t_z_list))

    # Print vertices
    x_list = np.array([0])
    y_list = np.array([0])
    z_list = np.array([0])
    for i in range(n):
        x_list = np.concatenate([x_list, [x_list[-1] + t_x_list[i] / n]])
        y_list = np.concatenate([y_list, [y_list[-1] + t_y_list[i] / n]])
        z_list = np.concatenate([z_list, [z_list[-1] + t_z_list[i] / n]])
    print()
    print("Vertices")
    print("x_list: {} ".format(x_list))
    print("y_list: {} ".format(y_list))
    print("z_list: {} ".format(z_list))

    p.plot_all(n, a, total_energy_history, ridge_energy_history, constr_1_history, constr_2_history, constr_3_history,
               constr_4_history, theta, phi, x_list, y_list, z_list, t_x_list, t_y_list, t_z_list)

    # save results
    if save_plots:
       # path for saving plot
       image_name = plot_home + '/{0}.svg'.format(run_name)
       plt.savefig(image_name)
       print('Plot has been saved in {0}'.format(image_name))

    print()
    print()
    print('---PROCESS COMPLETE---')
    print()
    print()

    if plot_show:
        plt.show()
