#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def chart():
   x = np.linspace(2, 10, 120)
   plt.plot(x, np.sin(x))
   plt.show() 