"""
This code is companion to the article "Ridge energy for thin nematic polymer networks", by
    Andrea Pedrini (andrea.pedrini@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy;
    Epifanio G. Virga (eg.virga@unipv.it) - Dipartimento di Matematica, Università di Pavia, via Ferrata 5, 27100 Pavia, Italy.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import lib.config as c


def plot_history(ax, title, history):
    """
    Plot history.

    Input
      ax: a matplotlib axis;
      title: a string;
      history: a numpy array.
    """
    x_attempts = list(range(len(history)))
    x_best = int(np.argmin(history))

    # ax.set_title(title)
    ax.plot(x_attempts, history, 'bo')
    ax.plot(x_best, history[x_best], 'ro')

    ax.set_title(title)
    ax.set(xlabel='attempts')
    ax.set_xlim(left=-1, right=len(history))
    return


def plot_angles(ax, theta, phi):
    """
    Plot angles theta and phi.

    Input
      ax: a matplotlib axis;
      theta: a numpy array;
      phi: a numpy array with same length as theta.
    """
    n = len(theta)
    ax.set_title('Best angles')
    ax.scatter(np.arange(n), theta, color='r', label=r'$\vartheta$')
    ax.scatter(np.arange(n), phi, color='g', label=r'$\varphi$')
    ax.set(xlabel='n')
    ax.set_xlim(left=-1, right=n)
    ax.legend()
    return


def plot_segments(ax, n, a, x_list, y_list, z_list, t_x_list, t_y_list, t_z_list):
    """
    Plot segments in 3D-space.

    Input
      ax: a matplotlib axis;
      n: an integer;
      a: a float;
      x_list: a numpy array with length n + 1;
      y_list: a numpy array with length n + 1;
      z_list: a numpy array with length n + 1;
      t_x_list: a numpy array with length n;
      t_y_list: a numpy array with length n;
      t_z_list: a numpy array with length n.
    """

    ax.set_title('Disembodied elastica')
    ax.scatter([0, 0], [0, 0], [0, a], zdir='z', s=100, c='red', depthshade=False)
    ax.quiver(x_list[:-1], y_list[:-1], z_list[:-1], t_x_list, t_y_list, t_z_list, length=1 / n, normalize=True,
              arrow_length_ratio=0.1, color='black')
    ax.scatter(x_list, y_list, z_list, zdir='z', s=70, c='blue', depthshade=False)
    return


def plot_all(n, a, total_energy_history, ridge_energy_history, constr_1_history, constr_2_history, constr_3_history,
             constr_4_history, theta, phi, x_list, y_list, z_list, t_x_list, t_y_list, t_z_list):
    """
    Plot statistics and best result.

    Input
      n: an integer;
      a: a float;
      total_energy_history: a numpy array;
      ridge_energy_history: a numpy array;
      constr_1_history: a numpy array;
      constr_2_history: a numpy array;
      constr_3_history: a numpy array;
      constr_4_history: a numpy array;
      theta: a numpy array;
      phi: a numpy array with same length as theta;
      x_list: a numpy array with length n + 1;
      y_list: a numpy array with length n + 1;
      z_list: a numpy array with length n + 1;
      t_x_list: a numpy array with length n;
      t_y_list: a numpy array with length n;
      t_z_list: a numpy array with length n.
    """
    # create figure
    fig = plt.figure(figsize=c.fig_size)
    fig.clear()

    # create subplots
    gs0 = gridspec.GridSpec(3, 5, width_ratios=[3, 1, 1, 1, 1], height_ratios=[1, 1, 0.5], )
    gs0.update(left=0.05, right=0.99, top=0.9, bottom=0.05, wspace=0.5, hspace=0.5)

    fig.suptitle('Disembodied elastica for n = {} and a = {}'.format(n, a), fontsize=16)

    ax_total_energy = plt.subplot(gs0[1, 0])
    ax_ridge_energy = plt.subplot(gs0[2, 0])
    ax_constr_1 = plt.subplot(gs0[2, 1])
    ax_constr_2 = plt.subplot(gs0[2, 2])
    ax_constr_3 = plt.subplot(gs0[2, 3])
    ax_constr_4 = plt.subplot(gs0[2, 4])
    ax_angles = plt.subplot(gs0[0, 0])
    ax_segments = plt.subplot(gs0[:2, 1:], projection='3d')
    # statistics
    plot_history(ax_total_energy, 'Total Energy', total_energy_history)
    plot_history(ax_ridge_energy, 'Ridge Energy', ridge_energy_history)
    plot_history(ax_constr_1, 'Constraint 1', constr_1_history)
    plot_history(ax_constr_2, 'Constraint 2', constr_2_history)
    plot_history(ax_constr_3, 'Constraint 3', constr_3_history)
    plot_history(ax_constr_4, 'Constraint 4', constr_4_history)
    # angles
    plot_angles(ax_angles, theta, phi)
    # segments
    plot_segments(ax_segments, n, a, x_list, y_list, z_list, t_x_list, t_y_list, t_z_list)

    return
