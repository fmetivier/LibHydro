# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 10:15:32 2014

@author: metivier
"""

from pylab import *
import numpy as np
from scipy.integrate import cumtrapz

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cmath
import pandas

def fn_lin(a=1, b=1):

    x = linspace(0, 10)

    phi = -8
    dphi = 2
    figure(figsize=(10, 10))
    for i in arange(20):
        P = phi + i * dphi
        # equipot
        y = (P - a * x) / b
        plot(x, y, "b-")
        lab = "$\Phi =  %s$" % P
        if 10 > (P - a * 10) / b > 0:
            text(10.1, (P - a * 10) / b, lab, color="blue")
        # courant
        y = (b * x - P) / (a)
        plot(x, y, "r-")
        lab = "$\Psi =  %s$" % P
        if 10 > (a * 10 - P) / (b) > 0:
            text((a * 10 - P) / (b), 10.1, lab, color="red", ha="center")

    Ux = [5, 5 - a]
    Uy = [5, 5 - b]
    arrow(5, 5, -a, -b, color="red", linewidth=3, width=0.01)
    text(5 - a / 2.0, 4.6 - b / 2.0, "U", color="red", size=16)
    axis([0, 10, 0, 10])
    savefig("../cours/figures/flownet.pdf", bbox_inches="tight")
    show()


def flow_net1(b=1):
    x = linspace(0.1, 10, 1000)

    figure(figsize=(10, 10))
    for i in arange(10) * 20:
        ypsi = sqrt(x ** 2 - i / b)
        plot(x, ypsi, "--", color='C3')
        if i % 2 == 0:
            lab = "$\Psi  =  %s$" % i
            text(10, sqrt(10 ** 2 - i / b), lab, color="C3")

    for i in arange(10) * (-20):
        ypsi = sqrt(x ** 2 - i / b)
        plot(x, ypsi, "C3--")

    for i in arange(10) * 20:
        yphi = i / (2 * b * x)
        plot(x, yphi, "-", color='C0')
        lab = "$\Phi = %s$" % i
        if 10 > i / (20 * b) > 0:
            text(i / (20 * b), 10.1, lab, color="C0", ha="center")

    axis([0, 10, 0, 10])
    show()


def flow_net2(b=1): 

    step = 5 * (arange(10) + 1)
    x = linspace(1, 20, 100)
    figure()
    for s in step:
        y = s / (2 * b * x)
        plot(x, y, "r-")
        psx = sqrt((b * x ** 2 + s) / b)
        plot(psx, x, "b-")

    show()



def puitscaptif():

    x = arange(50) + 41.0
    y = 0.05 * x + 0.5 * log((x - 40.5) ** 2)

    figure(figsize=(20, 5))
    plot(x, y, "b-")

    x = arange(41)
    y = 0.05 * x + 0.5 * log((x - 40.5) ** 2)
    plot(x, y, "b-")

    plot(arange(100), 0.05 * arange(100) + 4, "b-.")
    xlabel("Distance")
    ylabel("Charge")
    savefig("./rabattement1D.svg", bbox_inches="tight")
    show()




def test_C_plot():

    dmin = -10
    dmax = 10
    step = 0.1
    Z = []
    X = [arange(dmin, dmax, step) for y in range(len(arange(dmin, dmax, step)))]
    X = array(X)
    Y = X.transpose()
    for x in arange(dmin, dmax, step):
        row = []
        for y in arange(dmin, dmax, step):
            z = x + 1j * y
            z_ind = np.log(abs(x + 1j * y)) + 1j * cmath.phase(x + 1j * y)
            z_ind2 = np.sqrt(z)
            z_ind3 = np.log(abs(x - 20 + 1j * (y - 20))) + 1j * cmath.phase(
                (x - 20) + 1j * (y - 20)
            )
            z_4 = x - 1j * y
            # ~ row.append(z_ind+z_4)
            row.append(z_ind3)
        Z.append(row)

    Z = array(Z)

    v, u = np.gradient(Z.real)

    plt.figure()
    CS_phi = plt.contour(X, Y, Z.real, arange(20) - 7, colors=["blue"])
    plt.clabel(CS_phi, inline=1, fontsize=10)
    plt.streamplot(X, Y, -u, -v, density=0.5, color="red", linewidth=1)
    plt.contour(X, Y, Z.imag)
    plt.axis("equal")

    plt.figure()
    plt.imshow(Z.imag)

    plt.figure()
    plt.imshow(Z.real)

    plt.show()



def champs_CC2_g2():
    """Deux solution de Laplace
    phi = z^2 et phi = exp(y)cos(x)
    """

    cmap = cm.binary

    dmin = -10
    dmax = 10
    step = 0.1

    X = [arange(dmin, dmax, step) for y in range(len(arange(dmin, dmax, step)))]
    X = array(X)
    Y = X.transpose()

    u = X ** 2 - Y ** 2
    v = -2 * X * Y

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(231)
    c = ax.pcolor(X, Y, np.sqrt(u ** 2 + v ** 2), cmap=cmap)
    ax.streamplot(X, Y, u, v, density=1, color="blue", linewidth=1)
    # ~ ax.quiver(X,Y,u,v)
    plt.axis("square")
    ax.set_title("$(u,v)=(x^2-y^2,-2xy)$")
    ax.set_xlim(dmin, dmax)
    ax.set_ylim(dmin, dmax)
    plt.colorbar(c, label="$\sqrt{u^2+y^2}$")

    K = 1
    # ~ phi=(1/3)*X**3 - Y**2*X
    # ~ psi=X**2 * Y - Y**3 / 3
    phi = np.exp(Y) * np.cos(X)
    psi = np.exp(Y) * np.sin(X)

    fig2 = plt.figure()
    ax1 = fig2.add_subplot(111)
    lvl = range(0, 100, 20)
    C1 = ax1.contour(X, Y, phi, lvl, colors="C3")

    # ~ ax1.clabel(C1, lvl[1::2], inline=1, fontsize=10,fmt='%i')
    lvl = range(-100, 100, 10)
    C2 = ax1.contour(X, Y, psi, lvl, colors="C0")
    # ~ ax1.clabel(C2, lvl[1::2], inline=1, fontsize=10, fmt='%i')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title("b=1,K=1")
    plt.axis("square")


def RFU(d=1e-4,e=1e-6,L=1):

    cr = (np.pi/6)*((d+e)**3-d**3)
    RFU =  cr*(L/d)**3 

    print( RFU )


RFU(1e-5,1e-6,1)

def z2():
    """Exemple de fonction complexe donnent une solution de l'équation de Laplace
    """

    dmin = 0
    dmax = 10
    step = 0.01

    X = [arange(dmin, dmax, step) for y in range(len(arange(dmin, dmax, step)))]
    X = array(X)
    Y = X.transpose()

    phi = (X**2-Y**2)
    psi = (2*X*Y)

    fig, ax = plt.subplots(1, figsize=(10,10))
    c_phi  = ax.contour(X,Y,phi,(np.arange(10)-5)*20, colors = 'C3')
    for p in 20*np.arange(5):
        ax.text(dmax,np.sqrt(dmax**2-p), p, color='C3', va='center')
    c_psi = ax.contour(X,Y, psi,(np.arange(9)+1)*20, colors = 'C0')
    for s in (np.arange(9)+1)*20:
        ax.text(s/20, 10, s, color='C0',ha="center")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot([],[],'-', color='C3', label='$\Phi$')
    ax.plot([],[],'-', color='C0', label='$\Psi$')

    plt.legend(loc='lower left', fontsize=16)
    # plt.axis('equal')
    plt.grid('on')
    ax.set_xlim(dmin,dmax)
    ax.set_ylim(dmin,dmax)

    plt.savefig("./figures/z2.pdf", bbox_inches='tight')


def phys_ref():
    """Description du plan physique
    """

    Nz=5
    Nw=15

    fig, ax =plt.subplots(1,2,figsize=(10,5))
    ax[0].plot(3,2,'o', color='k')
    ax[0].arrow(0,0,3,2)
    ax[0].text(Nz+0.1,0,'$x$',va='center', fontsize=16)
    ax[0].text(0,Nz+0.1,'$y$',ha='center', fontsize=16)
    ax[0].text(3.1,2.1,"$z=x+iy$", fontsize=16, backgroundcolor='w')
    ax[0].set_xlim(0,Nz)
    ax[0].set_ylim(0,Nz)
    for i in range(Nz):
        ax[0].plot([0,Nz],[i,i],'--', color='k')
        ax[0].plot([i,i],[0,Nz],'--', color='k')
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)
    ax[0].set_title("Plan physique")

    ax[1].plot(6,10,'o', color='k')
    ax[1].arrow(0,0,6,10)
    ax[1].text(Nw+1,0,'$u$',va='center', fontsize=16)
    ax[1].text(0,Nw+1,'$w$',ha='center', fontsize=16)
    ax[1].text(6.2,10.2,"$w= f(z) = u(x,y)+iv(x,y)$", fontsize=16, backgroundcolor='w')
    ax[1].set_xlim(0,Nw)
    ax[1].set_ylim(0,Nw)
    for i in range(int(Nw/3)):
        ax[1].plot([0,Nw],[3*i,3*i],'--', color='k')
        ax[1].plot([3*i,3*i],[0,Nw],'--', color='k')

    ax[1].spines["top"].set_visible(False)
    ax[1].spines["right"].set_visible(False)
    ax[1].set_title("Plan mathématique")


    plt.savefig('./figures/plan_p_plan_m.pdf', bbox_inches = 'tight')

def w2():
    """fonction z = w^2 utilisée dans la solution de Kozeny
    """
    

    dmin = -1 # psi=1, phi=0
    dmax = 10 # artificiel
    step = 0.0001 # précision quand y-> 0

    phi_max = dmax/2
    xmax = phi_max**2

    r =dmax/xmax

    fig, ax = plt.subplots(1, figsize=(10,r*10))
    
    for psi in arange(5)/4:
        x = arange(dmin,(phi_max**2-psi**2),step)
        y = 2 * np.sqrt(x+psi**2) * psi  
        ax.plot(x,y,'-',color='C0')

    for phi in np.arange(11)*dmax/18:
        x = arange(dmin,(phi_max**2),step)
        y = 2 * np.sqrt(phi**2 - x) * phi 
        xmin = (4*phi**4-4 )/(4+4*phi**2)
        y = y[x>=xmin]
        x = x[x>=xmin]
        ax.plot(x,y,'-',color='C3')

    plt.plot([0,0],[-1,10],'--', color='k')
    plt.plot([-2,phi_max**2+1],[0,0],'--', color='k')
    ax.set_xlim(-2,phi_max**2+1)
    ax.set_ylim(-1,2*phi_max)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # plt.savefig("./figures/w2.pdf", bbox_inches = 'tight')
    # plt.axis("equal")

def w2_mapping():
    """mapping de  w^2 utilisée dans la solution de Kozeny
    """
    

    dmin = -1 # psi=1, phi=0
    dmax = 10 # artificiel
    step = 0.0001 # précision quand y-> 0

    phi_max = dmax/2
    xmax = phi_max**2

    qk = 1

    r =dmax/xmax
    w=15/2.54
    h=w/2

    fig, ax = plt.subplots(1,3, figsize=(w,h), width_ratios = [2,1,2])

    poly = Polygon([[0,0],[0,qk],[10,qk],[10,0],[0,0]], facecolor='lightgrey', edgecolor='w')
    ax[0].add_patch(poly)
    ax[0].plot([0,0],[0,qk], color='C1')
    ax[0].plot([0,10],[qk,qk], color='C0')    
    ax[0].plot([0,10],[0,0], color='C2')
    ax[0].set_xlabel("$u$")
    ax[0].set_ylabel("$v$")
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].plot(4,0.7,'ko')
    ax[0].plot([0,4],[0,0.7],'k--')
    ax[0].text(4.1,0.75,'$w=u+iv$')
    x = np.linspace(-qk,10,100)
    pl = [[0,0]]
    pl.append([-qk,0])
    for i in arange(len(x)):
        pl.append([x[i],np.sqrt(x[i] + qk**2)])
    pl.append([10,0])
    pl.append([0,0])
    print(pl)
    poly2 = Polygon(pl,facecolor='lightgrey', edgecolor='w')
    ax[2].add_patch(poly2)
    ax[2].plot([0,-qk],[0,0], color='C1')    
    ax[2].plot(x,np.sqrt(x + qk**2), color='C0')
    ax[2].plot([0,10],[0,0], color='C2')
    ax[2].plot(2,0.5,'ko')
    ax[2].plot([0,2],[0,0.5],'k--')
    ax[2].text(2.1,0.6,'$z=x+iy$')
    ax[2].set_xlabel("$x$")
    ax[2].set_ylabel("$y$")
    ax[2].set_xticks([])
    ax[2].set_yticks([])


    ax[1].spines["top"].set_visible(False)
    ax[1].spines["bottom"].set_visible(False)
    ax[1].spines["left"].set_visible(False)
    ax[1].spines["right"].set_visible(False)
    ax[1].set_xticks([])
    ax[1].set_yticks([])

    ax[2].spines["top"].set_visible(False)
    ax[2].spines["right"].set_visible(False)

    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)

    ax[1].arrow(0,1,1,0,width=0.05)
    ax[1].arrow(1,0,-1,0,width=0.05)
    ax[1].text(0.5,0.75,"$z = w^2$", ha='center', fontsize=14)
    ax[1].text(0.5,0.2,"$w = \sqrt{z}$", ha='center', fontsize=14)


    plt.savefig("./figures/z_w_transform.pdf", bbox_inches = 'tight')
    # plt.axis("equal")

def glover():
    """Solution de Glover d'un biseau salé
    """
    

    dmin = -1 # psi=1, phi=0
    dmax = 10 # artificiel
    step = 0.0001 # précision quand y-> 0
    a = 25/1000

    phi_max = dmax/2
    xmax = phi_max**2

    r =dmax/xmax

    fig, ax = plt.subplots(1, figsize=(10,r*10))
    
    for psi in arange(5)/4:
        x = arange(dmin,(phi_max**2-psi**2),step)
        y = - 2 * np.sqrt(x+psi**2) * psi / a  
        ax.plot(x,y,'-',color='C0')

    for phi in np.arange(11)*dmax/18:
        x = arange(dmin,(phi_max**2),step)
        y = - 2 * np.sqrt(phi**2 - x) * phi / a 
        xmin = (4*phi**4-4 )/(4+4*phi**2)
        y = y[x>=xmin]
        x = x[x>=xmin]
        ax.plot(x,y,'-',color='C3')

    plt.plot([0,0],[-1,10],'--', color='k')
    plt.plot([-2,phi_max**2+1],[0,0],'--', color='k')
    # ax.set_xlim(-2,phi_max**2+1)
    # ax.set_ylim(-1,2*phi_max)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # plt.savefig("./figures/glover.pdf", bbox_inches = 'tight')
    
def verruijt():

    gamma = 25/1000
    Q = 0.5
    k = 1
    R = (1+gamma)/(2*gamma)
    N=100
    nech=10

    fig,ax = plt.subplots(1)

    # surface libre AB
    y = np.linspace(0,2,100)
    x = -(Q/k)*(R)*(k*y/Q)**2

    xm = max(x)

    # ax.plot(x,y,'-', color='C0', zorder=2)

    # surface DE 
    y = np.linspace(0,-15,100)
    x = - (Q/k)*(R*gamma**2 *(k*y/Q)**2 - (1-gamma)/(2*gamma))

    xM = max(x)

    # ax.plot(x,y,'-', color='C0', zorder=2)
    ax.plot([xm,xM],[0,0],'-', color='C0')

    xmax = (Q/k)*(1-gamma)/2/gamma
    xmin = -20
    N = 1000
    dx = (xmax-xmin)/N
    x = linspace(xmin,xmax+dx,N)
    for psi in np.linspace(0,Q,10):
        y =  (1-2*R*psi/Q) * ( - (k*Q/R)*x -Q*psi/R + psi**2)**0.5
        # ax.plot(x,y,'-', color='C0')

    for phi in np.linspace(0,1,nech):
        x, y = [], []
        for psi in np.linspace(0,Q,N):
            x.append( -(R/(k*Q))*(phi**2-psi**2) - psi )
            y.append( phi/k - 2*R/(k*Q) * phi * psi)

        ax.plot(x,y,'-',color='C3')

    for psi in np.linspace(0,Q,nech):
        x, y = [], []
        for phi in np.linspace(0,1,N):
            x.append( -(R/(k*Q))*(phi**2-psi**2) - psi )
            y.append( phi/k - 2*R/(k*Q) * phi * psi)

        ax.plot(x,y,'-',color='C0')
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.plot([],[], '-', color='C0', label='$\Psi= Cte$')
    ax.plot([],[], '-', color='C3', label='$\Phi = Cte$')
    plt.legend()

    plt.savefig("../figures/verruijt.pdf", bbox_inches="tight")

######################################################################################
#  Guérin aquifère profond
######################################################################################
def plans_deep_aq():

    w=17/2.54
    h=w/3
    fig, ax = plt.subplots(1,3, figsize=(w,h))

    x= np.linspace(0,10,100)
    ax[0].plot(x,np.sqrt(x),'-', color='C0', lw=2)
    ax[0].plot(0,0,'o', color='C2')
    ax[0].plot([0,0],[0,-10],'-', color='C3', lw=2)
    ax[0].arrow(0,0, 10,0, ec='k', head_width=0.1, head_length=0.2)
    ax[0].arrow(0,0, 0, 5, ec='k', head_width=0.1, head_length=0.2)
    ax[0].text(5,-1,"x")
    ax[0].text(-1,2,"y")
    ax[0].text(1,-5,"$\Psi = 0$", color='C3')
    ax[0].text(5,3.5,"$\Phi = y,\ \Psi = q/K$", color='C0')
    plt.axis("equal")
    ax[1].plot([0,9],[0,0],'-',color='C3', lw=2)
    ax[1].plot([0,9],[9,9],'-',color='C0', lw=2)
    ax[1].plot([0,0],[0,9],'-',color='C2', lw=2)
    ax[1].arrow(0,0, 10,0, ec='k', head_width=0.1, head_length=0.2)
    ax[1].arrow(0,0, 0, 10, ec='k', head_width=0.1, head_length=0.2)
    ax[1].text(5,-1,"$\Phi$")
    ax[1].text(-1.5,5,"$\Psi$")
    ax[1].text(8,0.5,"$\Psi = 0$", color='C3')
    ax[1].text(8,9.5,"$\Psi  = q/K$", color='C0')
    plt.axis("equal")

    ax[2].arrow(0,0, 10,0, ec='k', head_width=0.1, head_length=0.2)
    ax[2].arrow(0,0, 0, 10, ec='k', head_width=0.1, head_length=0.2)
    ax[2].plot([0,9],[0,0],'-', color='C3', lw=2)
    ax[2].plot([0,0],[0,4],'-', color='C2', lw=2)
    ax[2].plot([0,0],[4,9],'-', color='C0', lw=2)
    ax[2].plot(0,4,'d', color='k', ms=4)
    ax[2].text(5,-1.5,"$\\theta_1$")
    ax[2].text(-1.5,6,"$\\theta_2$")
    ax[2].text(-0.5,4,"$q/K$", ha="right", va="center")
    ax[2].text(8,0.5,"$\Psi + x = 0$", color='C3')
    ax[2].text(1,8,"$\Phi -y = 0$", color='C0')
    plt.axis('equal')



    for i in range(3):
        ax[i].spines.top.set_visible(False)
        ax[i].spines.bottom.set_visible(False)
        ax[i].spines.left.set_visible(False)
        ax[i].spines.right.set_visible(False)
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    plt.savefig("../figures/guerin_plans.pdf", bbox_inches='tight')
    

def deep_aq():
    """Solution de Guérin (2015)
    """

    Q=1
    K=1
    N=100
    nech=10

    fig,ax = plt.subplots(1, figsize=(10/2.54,10/2.54))
    for Psi in np.linspace(0,Q,nech):
        phi = np.linspace(0,2,N)
        psi = np.ones(N)*Psi 
        w = phi+1j*psi 
        print(w)
        z = 1j*(w -(Q/np.sqrt(2)/K)*np.sqrt(np.cosh(np.pi*w*K/Q)-1))
        ax.plot(z.real, z.imag,'-',color='C0')

    for Phi in np.linspace(0,2,nech):
        psi = np.linspace(0,Q,N)
        phi = np.ones(N)*Phi 
        w = phi+1j*psi 
        print(w)
        z = 1j*(w -(Q/np.sqrt(2)/K)*np.sqrt(np.cosh(np.pi*w*K/Q)-1))
        ax.plot(z.real, z.imag,'-',color='C3')


    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.plot([],[], '-', color='C0', label='$\Psi= Cte$')
    ax.plot([],[], '-', color='C3', label='$\Phi = Cte$')
    plt.legend()
    plt.axis('equal')

    plt.savefig("../figures/guerin.pdf", bbox_inches='tight')

######################################################################################
#  Polu
######################################################################################

def polu_barrage_infini():

    Q = 1 # débit
    K = 1 # conductivité
    b = 1 # 1/2 largeur du barrage
    h = 1 # ecart de hauteur entre les plan de sortie et d'entrée
    N=100
    nech=10

    fig,ax = plt.subplots(1, figsize=(15/2.54,10/2.54))
    for Psi in np.linspace(0,Q,nech):
        phi = np.linspace(0,1,N)
        psi = np.ones(N)*Psi 
        w = phi+1j*psi 
        print(w)
        z = b * np.cos(np.pi*w/(K*h))
        ax.plot(z.real, z.imag,'-',color='C0')

    for Phi in np.linspace(0,1,nech):
        psi = np.linspace(0,Q,N)
        phi = np.ones(N)*Phi 
        w = phi+1j*psi 
        print(w)
        z = b * np.cos(np.pi*w/(K*h))
        ax.plot(z.real, z.imag,'-',color='C3')


    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.plot([],[], '-', color='C0', label='$\Psi= Cte$')
    ax.plot([],[], '-', color='C3', label='$\Phi = Cte$')
    plt.legend()
    plt.axis('equal')
    plt.savefig("../figures/polu_barrage_infini.pdf", bbox_inches='tight')


######################################################################################
#  Toth
######################################################################################


def toth(z0=1000, s = 2000, alpha = 0.01 , a = 20 , lam =500, n = 100):

    b = 2*np.pi/lam
    ap = a/np.cos(alpha)
    bp = b/np.cos(alpha)
    cp = np.tan(alpha)

    Phi_0 = z0 + cp*s/2 + (ap/(s*bp))*(1-np.cos(bp*s))

    x = np.linspace(0,s,100)
    z = np.linspace(0,z0,100)
    X,Z = np.meshgrid(x,z)
    Phi = X*0+Phi_0

    for i in np.arange(n):
        m=i+1
        Phi += 2* phi_n(m, ap, bp, cp, s)*np.cos(m*np.pi*X/s)*np.cosh(np.pi*m*Z/s)/(s*np.cosh(np.pi*m*z0/s))

    h=10/2.54
    w = 2*h
    fig,ax = plt.subplots(2,1, figsize=(w,h), height_ratios=[1,3])
    ax[1].contourf(X,Z,Phi, levels=30, cmap='Blues_r')
    V, U = np.gradient(Phi, z,x)
    ax[1].streamplot(X, Z, -U, -V, color='C3' , linewidth=0.5)
    ax[1].set_xlim(0,s)
    ax[1].set_ylim(0,z0)
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('z')
    ax[0].plot(x,z0+cp*x+ap*np.sin(bp*x),'k-')
    ax[0].set_xlim(0,s)
    ax[0].set_xticks([])
    ax[0].set_ylabel('$\phi$')
    plt.title("$z_0 = %i$,  $s = %i$, $\\alpha= %.2f$, $a =%i$, $ b = %.3f$" % (z0,s,alpha,a,2*np.pi/lam))
    
    # plt.savefig('../figures/toth_%i_%i_%i_%i_%i.pdf' % (z0,s,alpha*100,a,lam), bbox_inches='tight')

    fig, ax  = plt.subplots( figsize=(w,h))  
    Vm = np.mean(np.sqrt(V**2+U**2))
    
    cs = ax.contourf((np.diff(V)*100/z0+np.diff(U)*100/s)/Vm ) 
    plt.colorbar(cs, label="$\mathrm{div}(\mathbf{u})/\langle u \\rangle$")
    ax.set_xticks(np.arange(5)*20, np.arange(5)*400)
    ax.set_yticks(np.arange(5)*20, np.arange(5)*100)
    ax.set_xlabel('x')
    ax.set_ylabel('z')

    # plt.savefig('../figures/toth_conserv.pdf', bbox_inches='tight')


def toth_artesian(z0=1000, s = 2000, alpha = 0.01 , a = 20 , lam =500, n = 100):

    b = 2*np.pi/lam
    ap = a/np.cos(alpha)
    bp = b/np.cos(alpha)
    cp = np.tan(alpha)

    Phi_0 = z0 + cp*s/2 + (ap/(s*bp))*(1-np.cos(bp*s))

    x = np.linspace(0,s,100)
    z = np.linspace(0,z0,100)
    X,Z = np.meshgrid(x,z)
    Phi = X*0+Phi_0

    for i in np.arange(n):
        m=i+1
        Phi += 2* phi_n(m, ap, bp, cp, s)*np.cos(m*np.pi*X/s)*np.cosh(np.pi*m*Z/s)/(s*np.cosh(np.pi*m*z0/s))

    h=10/2.54
    w = 2*h
    fig,ax = plt.subplots(1,2, figsize=(w,h), width_ratios=[3,1])
    ax[0].contourf(X,Z,Phi, levels=30, cmap='Greys_r')
    V, U = np.gradient(Phi, z,x)
    ax[0].streamplot(X, Z, -U, -V, color='C3' , linewidth=0.5)
    ax[0].set_xlim(0,s)
    ax[0].set_ylim(0,z0)
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('z')
    p0=70
    for i in range(5):
        xp = (p0+i*2)*s/100
        ax[0].plot([xp,xp],[0,z0],'--')
        ax[1].plot(Phi[:,p0+i*2],z)
    ax[1].set_xlabel("$\Phi$")
    ax[1].set_ylim(0,z0)
    ax[1].set_yticks([])    
    plt.savefig('../figures/toth_%i_%i_%i_%i_%i_artesian.pdf' % (z0,s,alpha*100,a,lam), bbox_inches='tight')


    

def toth_boundaries(z0=1000, s = 2000, alpha = 0.02 , a = 10 , lam =500, n = 100):

    w=17/2.54
    h=w*z0/s
    b = 2*np.pi/lam
    ap = a/np.cos(alpha)
    bp = b/np.cos(alpha)
    cp = np.tan(alpha)

    x = np.linspace(0,s,100)
    z = z0+cp*x+ap*np.sin(bp*x) 
    zt = z + ap*np.exp(np.sin(bp*x) + np.pi/4) 

    fig, ax = plt.subplots(1, figsize=(w,h))
    ax.plot(x,zt,'k--', label="Topographie du versant")
    ax.plot(x,z,'k-', label="Surface libre de la nappe")
    ax.plot([0,s],[z0,z0],'k-.', label="Limite du domaine d'intégration")
    ax.set_xlim(0,s)
    ax.set_ylim(0,max(zt))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel('z')
    ax.set_xlabel('x')
    plt.legend()
    ax.text(-0.5,z0,"$z_0$", ha='right',va='center',fontsize=12)
    ax.text(0.05*s,z0/2,"$\\frac{\partial\phi}{\partial x} = 0$", ha='left',fontsize=14)
    ax.text(0.95*s,z0/2,"$\\frac{\partial\phi}{\partial x} = 0$", ha='right',fontsize=14)
    ax.text(2*s/3,0.1*z0,"$\\frac{\partial\phi}{\partial z} = 0$", ha='center',fontsize=14)
    ax.text(s/2,0.9*z0,"$\phi=\phi_t$")
    ax.spines.top.set_visible(False)



    plt.savefig('../figures/toth_boundaries.pdf', bbox_inches='tight')

def phi_n(m, ap, bp, cp,s):
    
    return ap*bp*(1-np.cos(bp*s)*np.cos(m*np.pi))/(bp**2 - m**2*np.pi**2 / s**2) + (cp * s**2)/(m**2 * np.pi**2)*(np.cos(m*np.pi)-1)




if __name__ == '__main__':
    # ~ exercice_sol_cc2()
    # probleme_cc2()
    # porosite_cc2()
    # ~ champs_CC2_g2()
    # ~ test_C_plot()

    # ~ milli2(20,20)
    # fay()
    # w2_mapping()
    # glover()
    # phys_ref()
    # verruijt()
    # plans_deep_aq()
    # deep_aq()
    # polu_barrage_infini()
    # for z in [100,500,1000]:
    # toth(z0 = 500)
    # toth_artesian(z0=500, s = 2000, alpha = 0.02 , a = 10 , lam =500, n = 100)
    # toth_boundaries()
    plt.show()
