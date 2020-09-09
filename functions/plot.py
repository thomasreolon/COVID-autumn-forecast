import numpy as np
import matplotlib.pyplot as plt


def plot_linear(y, deg=2, ylim=None, xlabel='time', ylabel='y'):
    # use polinomial regression
    x = [x for x in range(len(y))]
    cff = np.polyfit(x, y, deg)
    X = np.linspace(x[0], x[len(x)-1], 500)
    Y = np.zeros(len(X))
    for i, c in enumerate(cff):
        Y += c*X**(deg-i)

    # plot prediction
    plt.plot(X, Y, 'r')
    # plot datapoints
    plt.plot(x, y, 'bo')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # set maximum height
    if ylim:
        plt.ylim(0, ylim)
    plt.show()


def plot(y, xlabels, xlabel='x', ylabel='y', n_lab=5):
    # define xticks labels
    pr = int(len(y) / n_lab)
    xlabels = [v for i, v in enumerate(xlabels) if i % pr == 0][:n_lab]
    x = np.arange(n_lab)*pr
    ax = plt.gca()
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    # x,y labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # plot data
    plt.plot(np.arange(len(y)), y, 'r')
    plt.show()


def plot_multiple(points: list, columns=2, ylim=None, xlabel='time', ylabel='y'):
    # define image size
    B_SZ = 4
    rows = -(-len(points)//columns)
    fig = plt.figure(figsize=(B_SZ*columns, B_SZ*rows))

    # plot data in the list
    for i, y in zip(range(1, columns*rows + 1), points):
        fig.add_subplot(rows, columns, i)
        plt.plot(np.arange(len(y)), y, 'g')
        # styling
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if ylim:
            plt.ylim(0, ylim)
    plt.show()
