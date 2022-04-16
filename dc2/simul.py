#!/usr/bin/env python

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from random import sample
from numpy.random import uniform

def hopkins_statistic(X):
    
    X=X.values  #convert dataframe to a numpy array
    sample_size = int(X.shape[0]*0.05) #0.05 (5%) based on paper by Lawson and Jures
    
    
    #a uniform random sample in the original data space
    X_uniform_random_sample = uniform(X.min(axis=0), X.max(axis=0) ,(sample_size , X.shape[1]))
    
    
    
    #a random sample of size sample_size from the original data X
    random_indices=sample(range(0, X.shape[0], 1), sample_size)
    X_sample = X[random_indices]
   
    
    #initialise unsupervised learner for implementing neighbor searches
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs=neigh.fit(X)
    
    #u_distances = nearest neighbour distances from uniform random sample
    u_distances , u_indices = nbrs.kneighbors(X_uniform_random_sample , n_neighbors=2)
    u_distances = u_distances[: , 0] #distance to the first (nearest) neighbour
    
    #w_distances = nearest neighbour distances from a sample of points from original data X
    w_distances , w_indices = nbrs.kneighbors(X_sample , n_neighbors=2)
    #distance to the second nearest neighbour (as the first neighbour will be the point itself, with distance = 0)
    w_distances = w_distances[: , 1]
    
 
    
    u_sum = np.sum(u_distances)
    w_sum = np.sum(w_distances)
    
    #compute and return hopkins' statistic
    H = u_sum/ (u_sum + w_sum)
    return H

#CALIBRAZIONE HOPKINS
#sigma positivo: cluster; negativo: repulsione; nullo: PPP
#usate sigma interi. Più i sigma sono grandi, in valore assoluto, più vi allontanate dal processo stocastico

def hopkins_calibration(N=1000, sigma=0):

    N = int(N)      #Prelz dice sempre: venite incontro all'utente scemo. cast double in int
    v = np.zeros(N)

    #processo stocastico: PPP
    if sigma == 0:
        v = np.random.uniform(0,1,N)
    #Gaussiana centrata in 0.5, larghezza inversamente proporzionale a sigma
    if sigma > 0:
        stdev = 1/sigma
        v = np.random.normal(0.5,stdev,N)
        for i in range(N):
            while v[i]<0 or v[i]>1:
                v[i] = np.random.normal(0.5,stdev,1)
    #Dati equispaziati, con rumore gaussiano. Maggiore sigma (in modulo), più piccolo il rumore
    if sigma < 0:
        delta = 1/N
        stdev = delta/np.abs(sigma)
        dh = delta/2
        for i in range(N):
            v[i] = np.random.normal(dh + i*delta,stdev,1) 

    return v

#BARCODE PLOTS

n = 100
v0 = hopkins_calibration(n,0)
v1 = hopkins_calibration(n,10)
v2 = hopkins_calibration(n,-10)
#print(v0)

l = 400
code0 = np.zeros(l)
for i in range(l):
    for j in range(n):
        if v0[j] > i/l and v0[j] < (i+1)/l :
            code0[i]=1;
code1 = np.zeros(l)
for i in range(l):
    for j in range(n):
        if v1[j] > i/l and v1[j] < (i+1)/l :
            code1[i]=1;
code2 = np.zeros(l)
for i in range(l):
    for j in range(n):
        if v2[j] > i/l and v2[j] < (i+1)/l :
            code2[i]=1;

pixel_per_bar = 4
dpi = 100



fig0 = plt.figure(figsize=(len(code0) * pixel_per_bar / dpi, 2), dpi=dpi)
ax0 = fig0.add_axes([0, 0, 1, 1])  # span the whole figure
ax0.set_axis_off()
ax0.imshow(code0.reshape(1, -1), cmap='binary', aspect='auto',
          interpolation='nearest')

fig1 = plt.figure(figsize=(len(code1) * pixel_per_bar / dpi, 2), dpi=dpi)
ax1 = fig1.add_axes([0, 0, 1, 1])  # span the whole figure
ax1.set_axis_off()
ax1.imshow(code1.reshape(1, -1), cmap='binary', aspect='auto',
          interpolation='nearest')

fig2 = plt.figure(figsize=(len(code2) * pixel_per_bar / dpi, 2), dpi=dpi)
ax2 = fig2.add_axes([0, 0, 1, 1])  # span the whole figure
ax2.set_axis_off()
ax2.imshow(code2.reshape(1, -1), cmap='binary', aspect='auto',
          interpolation='nearest')



#CALIBRAZIONE SOGLIE

num = 1000
simulnum = 10000
H_P = np.zeros(simulnum)
H_C = np.zeros(simulnum)
H_R = np.zeros(simulnum)

#PPP

for i in range(simulnum):
    H_P[i]=hopkins_statistic(pd.DataFrame(hopkins_calibration(num,0)))

H_P = np.sort(H_P)
H_P_splice = H_P[int(simulnum*0.025 + 1):int(simulnum*0.975)]

figP, axP = plt.subplots(1, 1, figsize=(15, 10))
axP.hist(H_P)

print("H min Poisson: ", np.min(H_P), "\t H max Poisson: ", np.max(H_P))
print("H 2.5pct Poisson: ", np.min(H_P_splice), "\t H 97.5pct Poisson: ", np.max(H_P_splice))

#cluster (sigma 10)

for i in range(simulnum):
    H_C[i]=hopkins_statistic(pd.DataFrame(hopkins_calibration(num,10)))

H_C = np.sort(H_C)
H_C_splice = H_C[int(simulnum*0.025 + 1):int(simulnum*0.975)]

figC, axC = plt.subplots(1, 1, figsize=(15, 10))
axC.hist(H_C)

print("H min cluster: ", np.min(H_C), "\t H max cluster: ", np.max(H_C))
print("H 2.5pct cluster: ", np.min(H_C_splice), "\t H 97.5pct cluster: ", np.max(H_C_splice))

#repulsione (sigma -10)

for i in range(simulnum):
    H_R[i]=hopkins_statistic(pd.DataFrame(hopkins_calibration(num,-10)))

H_R = np.sort(H_R)
H_R_splice = H_R[int(simulnum*0.025 + 1):int(simulnum*0.975)]

figR, axR = plt.subplots(1, 1, figsize=(15, 10))
axR.hist(H_R)

print("H min repulsione: ", np.min(H_R), "\t H max repulsione: ", np.max(H_R))
print("H 2.5pct repulsione: ", np.min(H_R_splice), "\t H 97.5pct repulsione: ", np.max(H_R_splice))

plt.show()

