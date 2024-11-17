import matplotlib.pyplot as plt

def setup_plotting(title, xlabel, ylabel):
    plt.ion()
    fig, ax = plt.subplots(len(title), 1)
    
    for i in range(len(title)):
        ax[i].set_title(title[i])
        ax[i].set_xlabel(xlabel[i])
        ax[i].set_ylabel(ylabel[i])
        ax[i].grid()
    return fig, ax

