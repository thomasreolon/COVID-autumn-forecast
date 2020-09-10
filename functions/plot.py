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


def set_x_ticks(xlabels, n_lab, special=None):
    if xlabels:
        # define xticks labels
        pr = int(len(xlabels) / n_lab)
        x = [i for i, v in enumerate(xlabels) if i %
             pr == 0][:n_lab] + [len(xlabels)-1]
        xlabels = [v for i, v in enumerate(
            xlabels) if i % pr == 0][:n_lab] + [xlabels[-1]]
        if special:
            x.append(special[0])
            xlabels.append(special[1])
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
    X = np.linspace(x[0], x[-1], 100)
    Y = np.zeros(len(X))
    for i, c in enumerate(cff):
        Y += c*X**(deg-i)

    # set xticks
    set_x_ticks(xlabels, n_lab)

    # plot prediction
    plt.plot(X, Y, 'r')
    # plot datapoints
    plt.plot(x, y, 'bo')

    plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#616161")
    plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#616161")

    # set maximum height
    if ylim:
        plt.ylim(0, ylim)
    plt.show()


@with_style
def plot(y, xlabels, xlabel='x', ylabel='y', n_lab=5, style=None):
    plt.figure(figsize=(12, 4))

    # x,y labels
    set_x_ticks(xlabels, n_lab)
    plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#616161")
    plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#616161")

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


@with_style
def plot_prediction(y,  xlabels, xlabel='time', ylabel='y', n_lab=2, style=None):
    FP = 14  # how many days in the future
    # predict
    x = np.arange(len(y))
    cff = np.polyfit(x, np.log(y), 1, w=np.sqrt(y))
    X = np.linspace(x[0], x[-1]+FP, 100)
    Y = np.exp(cff[1])*np.exp(X*cff[0])

    # plot
    plt.plot(x, y, 'bo')
    plt.plot(X, Y, 'r')

    # add labels
    plt.xlabel(xlabel, labelpad=15, fontsize=11, color="#616161")
    plt.ylabel(ylabel, labelpad=15, fontsize=11, color="#616161")

    # calc date of prediction
    date = xlabels[-1]
    dd = (int(date[8:10]) + FP) % 30
    mm = int(date[5:7]) + ((int(date[8:10]) + FP) // 30)
    yy = int(date[0:4])
    if mm == 13:
        yy += 1
        mm = 1
    # set xticks
    date = "{}-{}-{}".format(yy, mm, dd)
    x_point = x[-1]+FP-1
    set_x_ticks(xlabels, n_lab, special=(x_point, date))

    # more emphasis to prediction
    label = "{} predicted\non the {}\n=\n {}".format(ylabel, date, int(Y[-1]))
    plt.annotate(label, (x_point, Y[-1]), color="#ab1346",
                 bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8),
                 textcoords="offset points", xytext=(-50, -50), ha='center'
                 )

    plt.show()
