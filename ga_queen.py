# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 16:10:49 2018

@author: Eric
"""

# Maximize  8≦x≦10; 9≦y≦12; x+y≦21 
# Maximum ≒ 46.0125 at (x,y)=(9.039,11.802)

import random
import matplotlib.pyplot as plt
import pandas as pd

# parameter settings
queen_num = 10
generation = 300

population = 100
parent_chromo = []
parent_objective_function_value = []
min_objective_function_value = []
best_objective_function_value = []
best_chromo = []
parent_normalize = []
parent_accumulation = []

######################################################################################
# Functions

# calculate the value of objective function
def evaluation(n,queen_pos):
    forw_sum_of_queen_pos = []
    back_sum_of_queen_pos = []
    penalty = 0
    
    # calculate forward sum of position
    for i in range(len(queen_pos)):
        x = i
        y = queen_pos[i]
        forw_sum_of_queen_pos.append(x+y)
    
    # calculate backward sum of position
    for i in range(len(queen_pos)):
        for j in range(1,len(queen_pos)+1):
            if queen_pos[i] == queen_pos[-j]:
                x = j-1
                y = queen_pos[i]
        back_sum_of_queen_pos.append(x+y)
    
    # calculate forward penalty
    for i in range((len(queen_pos)-1)*2):
        count = 0
        for j in forw_sum_of_queen_pos:
            if i == j:
                count += 1
        if count > 1:
            penalty += count*(count-1)/2
            
    # calculate backward penalty
    for i in range((len(queen_pos)-1)*2):
        count = 0
        for j in back_sum_of_queen_pos:
            if i == j:
                count += 1
        if count > 1:
            penalty += count*(count-1)/2
            
    objective_value = penalty
    return objective_value

# crossover function
def _repeated(element, collection):
    c = 0
    for e in collection:
        if e == element:
            c += 1
    return c > 1
 
def _swap(data_a, data_b, cross_points):
    c1, c2 = cross_points
    new_a = data_a[:c1] + data_b[c1:c2] + data_a[c2:]
    new_b = data_b[:c1] + data_a[c1:c2] + data_b[c2:]
    return new_a, new_b
 
def _map(swapped, cross_points):
    n = len(swapped[0])
    c1, c2 = cross_points
    s1, s2 = swapped
    map_ = s1[c1:c2], s2[c1:c2]
    for i_chromosome in range(n):
        if not c1 < i_chromosome < c2:
            for i_son in range(2):
                while _repeated(swapped[i_son][i_chromosome], swapped[i_son]):
                    map_index = map_[i_son].index(swapped[i_son][i_chromosome])
                    swapped[i_son][i_chromosome] = map_[1-i_son][map_index]
    return s1, s2
  
def pmx(parent_a, parent_b):
    assert(len(parent_a) == len(parent_b))
    n = len(parent_a)
#    seg = int(n*0.3)
    cross_points = sorted([int(n*0.3) , int(n*0.8)])
    swapped = _swap(parent_a, parent_b, cross_points)
    mapped = _map(swapped, cross_points)
 
    return mapped
# crossover function
    
# update function
def generate_child(parent,child,queen_num,parent_accumulation,population):
    for k in range(int(population/2)):
        wheel1 = random.uniform(1,max(parent_accumulation))
        wheel2 = random.uniform(1,max(parent_accumulation))
        for i in parent_accumulation:
            if i > wheel1:
                chosen_index1 = parent_accumulation.index(i)
                break
        for i in parent_accumulation:
            if i > wheel2:
                chosen_index2 = parent_accumulation.index(i)
                break
        child.extend(pmx(parent[chosen_index1],parent[chosen_index2]))
    for k in child:
        mutate_index = random.sample(range(queen_num), 2)
        k[mutate_index[0]],k[mutate_index[1]] = k[mutate_index[1]], k[mutate_index[0]]
    return child
    
#####################################################################################

# Main Program
# initialization part
for i in range(population):
    rand_solution = random.sample(range(0,queen_num),queen_num)
    rand_solution_obj = evaluation(queen_num,rand_solution)
    parent_chromo.append(rand_solution)
    parent_objective_function_value.append(rand_solution_obj)
    
for i in parent_objective_function_value:
    if i != 0:
        parent_normalize.append((sum(parent_objective_function_value))/i)
    else:
        parent_normalize.append((sum(parent_objective_function_value))/0.1)
parent_accumulation = [sum(parent_normalize[:i]) for i in range(1, len(parent_normalize) + 1)]
    
min_value = min(parent_objective_function_value)
min_objective_function_value.append(min_value)
best_objective_function_value.append(min_value)
best_index = parent_objective_function_value.index(min_value)
best_chromo.append(parent_chromo[best_index])

child_chromo = []
parent_chromo = generate_child(parent_chromo,child_chromo,queen_num,parent_accumulation,population)

for i in range(generation-1):
    parent_objective_function_value = []
    parent_accumulation = []
    parent_normalize = []
    
    for j in range(population):
        parent_fitness = evaluation(queen_num,parent_chromo[j])
        parent_objective_function_value.append(parent_fitness)
        
    for j in parent_objective_function_value:
        if i != 0:
            parent_normalize.append((sum(parent_objective_function_value))/i)
        else:
            parent_normalize.append((sum(parent_objective_function_value))/0.1)
    parent_accumulation = [sum(parent_normalize[:i]) for i in range(1, len(parent_normalize) + 1)]
    
    min_value = min(parent_objective_function_value)
    min_objective_function_value.append(min_value)
    if best_objective_function_value[i] > min_value:
        best_objective_function_value.append(min_value)
        best_index = parent_objective_function_value.index(min_value)
        best_chromo.append(parent_chromo[best_index])
    else:
        best_objective_function_value.append(best_objective_function_value[i])
        best_chromo.append(best_chromo[i])
    
    child_chromo = []
    parent_chromo = generate_child(parent_chromo,child_chromo,queen_num,parent_accumulation,population)

# Plot
fig = plt.figure(figsize=(20,8))
ax = fig.add_subplot(1,1,1)
ax.plot(best_objective_function_value,'r',linewidth=4, alpha=0.8,label='Best Record')
ax.plot(min_objective_function_value,'b-o',linewidth=2.5, alpha=0.6,label='Max Value/Generation')
ax.legend()
ax.grid()
print("best route : ",best_chromo[generation-1])
print("f : " ,best_objective_function_value[generation-1])

## Boxplot
#fig = plt.figure(1, figsize=(9, 6))
## Create an axes instance
#ax = fig.add_subplot(111)
#bp = ax.boxplot(min_objective_function_value)
#ax.set_xticklabels('PSO')

#boxp = pd.DataFrame()
#boxp['iteration'] = range(1,301)
#boxp['obj_value'] = pd.Series(min_objective_function_value)
#boxp.to_csv('ga_boxplot.csv', index = False)
