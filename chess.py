# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 15:41:57 2018

@author: Rod
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from IPython.display import HTML
import numpy as np
import pandas as pd
import copy
import math
import random as rnd
import time
%matplotlib inline
import re

#%%
file = open('300permutation.txt')
lines = file.readlines()
per300 = []
i = 0
for line in lines :
    num = list(map(int, re.findall(r'\d+', line)))
    per300.append(num)
#%%
i = 0
for solution in per300[:5]:
    i += 1
    #solution = [1,3,4,3,4,5,7,8,9,1,10,12,13,14]
    #solution = [i-1 for i in solution]
    chessboard_size = len(solution)
    chessboard = np.full((chessboard_size**2), 0.5)
    #create checkered board
    if chessboard_size % 2 != 0:
        chessboard[::2] = 1
        chessboard = chessboard.reshape((chessboard_size, chessboard_size))
    else:
        chessboard = chessboard.reshape((chessboard_size, chessboard_size))
        for i in range(len(chessboard)):
            if (i % 2) != 0:
                chessboard[i][1::2] = 1
            else:
                chessboard[i][::2] = 1
    #
    index_x = np.arange(n)
    index_y = solution
    #
    x= index_x
    y= index_y
    
    for i in range(len(chessboard)):
        chessboard[x[i]][y[i]-1] = 0
    chessboard = chessboard.T
    z = chessboard.copy()

    #Creating plot for last Simulated Annealing
    fig = plt.figure(figsize = (20,20))
    ax = fig.add_subplot(111)
    ax.matshow(z, cmap = "RdGy")
    x = np.arange(chessboard_size)
    solution1 = [i-1 for i in solution]
    for i in range(len(z)):
        ax.text(x[i] ,solution1[i], s=u"\u2655", fontsize = 50, color = 'white', va='center', ha='center')
