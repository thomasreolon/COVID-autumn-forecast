import numpy as np
import matplotlib.pyplot as plt


def with_style(func):
    def wrapper(*args, **kw):
        done = False
        if 'style' in kw:
            style = kw['style']
            if style:
                with plt.style.context(style):
                    func(*args, **kw)
                    done = True

        if not done:
            func(*args, **kw)

    return wrapper


@with_style
def set_x_ticks(xlabels, n_lab, style=None):
    if xlabels:
        # define xticks labels
        pr = int(len(xlabels) / n_lab)
        x = [i for i, v in enumerate(xlabels) if i %
             pr == 0][:n_lab] + [len(xlabels)-1]
        xlabels = [v for i, v in enumerate(
            xlabels) if i % pr == 0][:n_lab] + [xlabels[-1]]
        ax = plt.gca()
        ax.set_xticks(x)
        ax.set_xticklabels(xlabels)
        plt.setp(ax.get_xticklabels(), rotation=30,
                 horizontalalignment='right')


@with_style
def plot_linear(y, deg=2, ylim=None, xlabel='time', ylabel='y', xlabels=None, n_lab=5, style=None):
    # use polinomial regression
    x = [x for x in range(len(y))]
    cff = np.polyfit(x, y, deg)
    X = np.linspace(x[0], x[len(x)-1], 500)
    Y = np.zeros(len(X))
    for i, c in enumerate(cff):
        Y += c*X**(deg-i)

    # set xticks
    set_x_ticks(xlabels, n_lab)

    # plot prediction
    plt.plot(X, Y, 'r')
    # plot datapoints
    plt.plot(x, y, 'bo')

    plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#333533")
    plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#333533")

    # set maximum height
    if ylim:
        plt.ylim(0, ylim)
    plt.show()


@with_style
def plot(y, xlabels, xlabel='x', ylabel='y', n_lab=5, style=None):
    plt.figure(figsize=(12, 4))

    # x,y labels
    set_x_ticks(xlabels, n_lab)
    plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#333533")
    plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#333533")

    # plot data
    plt.plot(np.arange(len(y)), y, 'r')
    plt.show()


@with_style
def plot_multiple(points: list, columns=2, ylim=None, xlabel='time', ylabel='y',  xlabels=None, n_lab=5, style=None):
    B_SZ = 5
    rows = -(-len(points)//columns)
    fig = plt.figure(figsize=(B_SZ*columns, B_SZ*rows))

    # plot data in the list
    for i, y in zip(range(1, columns*rows + 1), points):
        xticks = xlabels
        if isinstance(xticks, list):
            xticks = xticks[i-1]
        fig.add_subplot(rows, columns, i)
        plt.plot(np.arange(len(y)), y, 'g')
        # styling
        set_x_ticks(xticks, n_lab)
        plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#616161")
        plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#616161")
        if ylim:
            plt.ylim(0, ylim)
    fig.tight_layout()

    plt.show()
