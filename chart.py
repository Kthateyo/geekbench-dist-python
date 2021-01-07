from operator import mul
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()

def kde(cpu_names, singles, multies):

    dfs = []
    for i in range(len(cpu_names)):
        dfs.append(pd.DataFrame(singles[i], columns=[cpu_names[i]]))
    singles = pd.concat(dfs) if (len(cpu_names) > 1) else dfs[0]

    dfs = []
    for i in range(len(cpu_names)):
        dfs.append(pd.DataFrame(multies[i], columns=[cpu_names[i]]))
    multies = pd.concat(dfs) if (len(cpu_names) > 1) else dfs[0]

    # make a list of all dataframes 
    fig, axes = plt.subplots(2, 1)

    bw1 = 0.025
    bw2 = bw1 * 2

    singles.plot.kde(bw_method=bw1, xlim=(min(list(singles.min())), max(list(singles.max()))), ax=axes[0])
    multies.plot.kde(bw_method=bw2, xlim=(min(list(multies.min())), max(list(multies.max()))), ax=axes[1], legend=False)

    axes[0].set_title("Single Core Score")
    axes[1].set_title("Multi Core Score")
    

    plt.tight_layout()
    plt.show()

