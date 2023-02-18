import numpy as np
import matplotlib.pyplot as plt
import random
import streamlit as st
def Eval(d, c, n):
    Z = 0
    for kc in range(n-1):
        Z = Z + d[c[kc]-1,c[kc+1]-1]
    Z = Z + d[c[n-1]-1,c[0]-1]
    return Z

def Voisin(c, n):
    Ip = np.floor(1 + n * np.random.rand())
    Jp = np.floor(1 + n * np.random.rand())
    mx = int(max(Ip, Jp))
    mn = int(min(Ip, Jp))
    
    testV = np.random.rand()
    if testV < 0:
        Jp = Ip + 1
    cc = c.copy()
    cc[mn-1:mx] = np.flip(cc[mn-1:mx])
    cycleV = cc
    return cycleV

#==================
def Prendre(cout, coutcourant, T):
    delta_cout = cout - coutcourant
    p = np.random.rand()
    v = False
    if delta_cout > 0:
        if p < np.exp(-delta_cout/T):  
            v = True 
    if delta_cout < 0:
        v = True
    return v
#=====================
def palier(Tc, aT):
    return Tc * aT
#======================
def plotGraf(cycle, xpos, ypos):
    cas = 3
    fig=plt.figure(figsize=(5,5))
    plt.figure(cas)
    graf = np.concatenate((cycle, [cycle[0]]))
    xpos_=np.array(xpos)
    ypos_=np.array(ypos)
    plt.plot(xpos_[graf[:,0]-1], ypos_[graf[:,0]-1])
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)
    plt.title('Chemin le meilleur obtenu')