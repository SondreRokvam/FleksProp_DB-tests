# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:39:01 2020

@author: Sondre
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
cmaps = OrderedDict()

cmaps['PickedColors'] = ['hsv','tab20']
nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps.items())
gradient = np.linspace(0, 1, 20)
gradient = np.vstack((gradient, gradient))

def plot_color_gradients(cmap_category, cmap_list, nrows):
    fig, axes = plt.subplots(nrows=nrows)
    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))




for cmap_category, cmap_list in cmaps.items():
    print(cmap_category, cmap_list)
    plot_color_gradients(cmap_category, cmap_list, nrows)

plt.show()