# -*- coding: utf-8 -*-
"""
Created on "2020-05-27"

@author: metivier

Functions used to solve some of the problem of my Hydrogeology course book
https://hal.science/cel-01877908v13

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pch

def sol_plateau1S():

    h1 = 10
    h2 = 15
    L = 1000
    K = 1e-4
    P = [0/(352.25*86400),0.4/(352.25*86400)]
    o = 0.2

    C=('c','b')

    x=np.arange(10000)/10
    print(x)

    fig = plt.figure(figsize=(15/2.54, 5/2.54))
    ax=fig.add_subplot(111)

    for p , c  in zip(P,C):
        h = np.sqrt( (p/(K*o))*(L*x-x**2) + (h2**2 - h1**2)*x/L + h1**2 )
        ax.plot(x,h,'-',color = c )

    leg=['P = 0 m/a','P = 0.4 m/A']
    plt.legend(leg,loc='lower right')
    plt.show()

def sol_ile():

    R = 1000
    P = 0.5/(352.25*86400)
    K = 1e-4
    o = 0.2
    Q = 0.04

    r=np.arange(10000)/10 + 0.1

    fig = plt.figure(figsize=(10/2.54, 5/2.54))
    ax=fig.add_subplot(111)

    h = (P/(K*o))*(R**2-r**2)

    hp = Q/(np.pi * K) * np.log(r/R)


    ax.plot(r,np.sqrt(h+hp),'b-')
    ax.plot(-r,np.sqrt(h+hp),'b-')
    # plt.axis('square')

    plt.savefig("./figures/Ile.pdf")
    plt.show()



def annulus_fig():

    fig = plt.figure(figsize=(10/2.54,10/2.54))
    ax = fig.add_subplot(111)

    circle=plt.Circle([0,0],radius=10,fc='cornflowerblue',ec='k')
    ax.add_artist(circle)
    circle=plt.Circle([0,0],radius=5,fc='white',ec='k')
    ax.add_artist(circle)

    ax.plot([0,5],[0,0],'k--')
    ax.text(5.5,0,'$R_p,\ \phi=\Phi_p$')
    ax.plot([0,10*np.cos(np.pi/6)],[0,10*np.sin(np.pi/6)],'k--')
    ax.text(10.5*np.cos(np.pi/6),10.5*np.sin(np.pi/6),'$R_a,\ \phi=\Phi_a$')

    ax.text(0,7,"Region of flow", ha='center')

    ax.axis('square')

    ax.set_xlim(-12,12)
    ax.set_ylim(-12,12)

    ax.axis("off")
    plt.savefig("./figures/annulus_domain.pdf",bbox_inches='tight')
    plt.show()


def por_fig():
    """
    exercice 8.3 question e
    """

    ld = np.linspace(-5,-2,100)
    d=10**ld

    wt = 1 - np.pi/6
    we = wt - np.pi * 1e-6 / d
    cr =  np.pi * 1e-6 / d
    fig=plt.figure(figsize=(10/2.54,7/2.54))
    ax=fig.add_subplot(111)
    ax.loglog(d,we,'r--',label='Porosité efficace')
    # ax.loglog(d,cr,'g--')
    ax.loglog([1e-5,1e-2],[wt,wt],'k-',label='Porosité totale')
    ax.set_xlabel('Diamètre (m)')
    ax.set_ylabel('Porosité (%)')
    plt.legend(loc='lower right')

    plt.savefig("figures/ex8-3.pdf", bbox_inches='tight')
    plt.show()

def triangulation():

    fig=plt.figure(figsize=(7/2.54,7/2.54))
    ax=fig.add_subplot(111)

    h1 = [1000,5000,100]
    h2 = [4000,4000,90]
    h3 = [500,500,80]

    ax.plot(h1[0],h1[1],'bo')
    ax.text(1.2*h1[0],h1[1],'h1=100m')
    ax.plot(h2[0],h2[1],'bo')
    ax.text(1.1*h2[0],h2[1],'h2=90m')
    ax.plot(h3[0],h3[1],'bo')
    ax.text(1.4*h3[0],h3[1],'h3=80m')
    ax.plot([h1[0],h2[0],h3[0],h1[0]],[h1[1],h2[1],h3[1],h1[1]],'b-')

    # look for position
    d13 = np.sqrt((h1[0]-h3[0])**2+(h1[1]-h3[1])**2)
    print(d13)
    gr = d13/(h1[2]-h3[2])
    print(gr)

    # distance to the 90m isopieze
    d90 = 10*gr
    print(d90)

    # angle of the line h1-h3
    a = (h1[1]-h3[1])/(h1[0]-h3[0])
    print(a)

    # get the coordinate of h90
    dx = np.sqrt(d90**2/(1+a**2))
    dy = a*dx
    h90 = [h3[0]+dx,h3[1]+dy,90]


    # find slope of 90m piezometric line
    a2 = (h2[1]-h90[1])/(h2[0]-h90[0])
    # then calculat the slope of the perpendicular to the piozometric line
    ap2 = -(h2[0]-h90[0])/(h2[1]-h90[1])

    # find the intersect between 100 and 90m piezometric line
    x_int =  (-h1[1]+h90[1]+ap2*h1[0]-a2*h90[0]) / (ap2-a2)
    y_int = ap2*(x_int-h1[0])+h1[1]

    # find U
    d_1_int = np.sqrt((h1[0]-x_int)**2+(h1[1]-y_int)**2)
    K=1e-5
    U =  K * (10/d_1_int)
    # find middle of 90m segment to place the vector
    c = [0.5*(h2[0]+h90[0]),0.5*(h2[1]+h90[1]),90]

    # plot a vector that is colinear to U
    dx = 500
    dy = ap2*(dx)
    print(U)

    # plot
    ax.plot(h90[0],h90[1],'ro')
    ax.plot([h2[0], h90[0]],[h2[1],h90[1]],'r--')
    ax.plot(x_int,y_int,'ro')
    ax.plot([h1[0],x_int],[h1[1],y_int],'r--')
    ax.arrow(c[0],c[1],dx,dy,width=100)
    ax.text(1.1*(c[0]+0.6*dx),(c[1]+0.6*dy),"$\\vec{U}$")
    #

    ax.set_xlabel('x-distance (m)')
    ax.set_ylabel('y-distance (m)')
    ax.set_xlim(0,6000)
    ax.set_ylim(0,6000)

    plt.savefig("figures/triangul_corr.pdf", bbox_inches='tight')

    plt.show()

def laplace_signification():


    x=np.linspace(1,10,100)
    y1=x**3+100
    y2 = x/x
    y3 = (-x**3)+1000

    fig = plt.figure(figsize=(17/2.54,5/2.54))
    ax = fig.add_subplot(131)
    ax.plot(x,y1,'-')
    ax.plot([x[10],x[90]],[y1[10],y1[90]],'r--')
    ax.plot([x[50],x[50]],[0, 0.5*(y1[10]+y1[90])],'k--')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.setp(ax,xticks=[x[10],x[50],x[90]],xticklabels=['$x_1$','$x$','$x_2$'])
    ax.text(x[50]+0.5,y1[50],'y')
    ax.text(x[50]+0.5,0.5*(y1[10]+y1[90]),'$(y_1+y_2)/2$')
    ax.set_ylabel('$y=f(x)$')
    ax.set_ylim(0,1200)
    ax.set_title("$d^2f/dx^2 >0$")
    ax = fig.add_subplot(132)
    ax.plot(x,y2,'-')
    ax.plot([x[10],x[90]],[y2[10],y2[90]],'r--')
    ax.plot([x[50],x[50]],[0, 0.5*(y2[10]+y2[90])],'k--')
    ax.text(x[50],y2[50]+0.15,'y')
    ax.text(x[50],y2[50]-0.25,'$(y_1+y_2)/2$')

    ax.set_ylim(0,2)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.setp(ax,xticks=[x[10],x[50],x[90]],xticklabels=['$x_1$','$x$','$x_2$'])
    # ax.set_xlabel('$x$')
    ax.set_title("$d^2f/dx^2 = 0$")
    ax = fig.add_subplot(133)
    ax.plot(x,y3,'-')
    ax.plot([x[10],x[90]],[y3[10],y3[90]],'r--')
    ax.plot([x[50],x[50]],[0, y3[50]],'k--')
    ax.set_ylim(0,1200)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(x[50]+0.5,y3[50],'y')
    ax.text(x[50]+0.5,0.5*(y3[10]+y3[90]),'$(y_1+y_2)/2$')
    plt.setp(ax,xticks=[x[10],x[50],x[90]],xticklabels=['$x_1$','$x$','$x_2$'])
    ax.set_title("$d^2f/dx^2  < 0$")

    plt.savefig("figures/sig_laplace.pdf",bbox_inches="tight")
    plt.show()

def laplace_solution_captive():

    fig=plt.figure(figsize=(14/2.54,7/2.54))
    ax=fig.add_subplot(111)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([0,1,1,0,0],[0,0,1,1,0],'k-')
    ax.text(-0.15,0.5, '$\phi = h_1$')
    ax.text(1.01,0.5, '$\phi = h_2$')
    ax.arrow(0.5,0.8,0,0.3,width=0.01)
    ax.text(0.51,0.9,'$\partial_y\phi = 0$')
    ax.arrow(0.5,0.2,0,-0.3,width=0.01)
    ax.text(0.51,0.1,'$\partial_y\phi = 0$')
    ax.set_xlim(-0.2,1.2)
    ax.set_ylim(-0.2,1.2)
    ax.axis('off')

    plt.savefig("figures/laplace_solution_captive.pdf",bbox_inchez='tight')


    fig=plt.figure(figsize=(14/2.54,7/2.54))
    ax=fig.add_subplot(111)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot([0,1,1,0,0],[0,0,1,1,0],'k-')
    for i in range(7):
        ax.plot([i/6,i/6],[0,1],'b-')
        ax.plot([0,1],[i/6,i/6],'r--')

    ax.text(1.02,0.5,'$\psi=Cte$',color='r',va='center')
    ax.text(0.5,1.03,'$\phi=Cte$',color='b',ha='center')
    ax.set_xlim(-0.2,1.2)
    ax.set_ylim(-0.2,1.2)
    ax.axis('off')

    plt.savefig("figures/laplace_solution_captive_ec.pdf",bbox_inchez='tight')

    plt.show()

def termes():

    f = plt.figure()
    ax=f.add_subplot(111)
    ax.autoscale(enable=True)
    plt.axis('off')
    # r = f.canvas.get_renderer()
    t = plt.text(0, 0, 'zone saturée')

    # bb = t.get_window_extent(renderer=r)
    # width = bb.width
    # height = bb.height

    # print(width,height)

    # ax.set_xlim(0,width)
    # ax.set_ylim(0,height)

    ax.set_xticks([])
    ax.set_yticks([])


    plt.savefig('./test.png',bbox_inches='tight')

def solution_dupuit_deux_puits():

    p1=34
    p2=29
    L=2500
    z1 = 33
    z2 = 27
    h1=95
    h2=93

    phi1=h1-z1
    phi2=h2-z2
    dphi = phi1-phi2

    dp=p1-p2
    D = np.sqrt( dp**2 + L**2 )



    J = dphi/Dsinh

    Jh = dphi/L
    Jv = dphi/dp

    print(J,Jh,Jv,J-np.sqrt(Jh**2+Jv**2))

def solution_lac_0():
    """Solution lac 0 

    h1h1h1
    0    0
    0    0
    Pas de fond
    """

    L=200
    H=400
    N=100
    xi=np.linspace(0,L,100)
    yi=np.linspace(-H,0,100)

    x,y = np.meshgrid(xi,yi)



    phi=0*x

    h1=20

    phiH=np.zeros(100)
    c=np.zeros(N)


    for i in range(N):
        c[i] = 4*h1/((2*i+1)*np.pi)
        print (2*i+1,c[i])
        phi += c[i]*np.exp((2*i+1)*np.pi*y/L)*np.sin((2*i+1)*np.pi*x/L)

        phiH += 4*h1/((2*i+1)*np.pi) * np.sin((2*i+1)*np.pi*xi/L)


    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,28/2.54))
    ax = fig.add_subplot(111)
    bins = np.arange(h1)+1
    CS = ax.contour(x,y,phi, levels=[0.1,0.3,1,3,10], colors='C0')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='C3',density=0.5)
    # ax.axis('square')
    # ax.set_xlim(0,L)
    # ax.set_ylim(0,H)
    # ax.set_xlabel('Distance x')
    # ax.set_ylabel('Profondeur y')

    ax.axis('off')

    plt.savefig('./figures/Lac0.pdf',bbox_inches='tight')


def solution_lac_1():
    """Solution lac 1 

    h1h1h1
    0    0
    0    0
    000000
    """

    L=200
    H=100
    N=100
    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)



    phi=0*x

    h1=20

    phiH=np.zeros(100)
    c=np.zeros(N)


    for i in range(N):
        c[i] = 4*h1/((2*i+1)*np.pi*np.sinh((2*i+1)*np.pi*H/L))
        print (2*i+1,c[i])
        phi += c[i]*np.sinh((2*i+1)*np.pi*y/L)*np.sin((2*i+1)*np.pi*x/L)

        phiH += 4*h1/((2*i+1)*np.pi) * np.sin((2*i+1)*np.pi*xi/L)


    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    bins = np.arange(h1)+1
    CS = ax.contour(x,y,phi, levels=[1,5,10,15], colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')
    ax.set_xlim(0,L)
    ax.set_ylim(0,H)
    # ax.set_xlabel('Distance x')
    # ax.set_ylabel('Profondeur y')

    ax.axis('off')

    plt.savefig('./figures/Lac1.pdf',bbox_inches='tight')

    # ax2 = fig.add_subplot(212)
    # ax2.plot(xi,phiH,'r-')


    plt.show()

def solution_lac_2():

    L=200
    H=100
    N=100
    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)



    phi=0*x

    h1=20

    phiH=np.zeros(100)
    c=np.zeros(N)


    for i in range(N):
        c[i] = 4*h1/((2*i+1)*np.pi*np.cosh((2*i+1)*np.pi*H/L))
        print (2*i+1,c[i])
        phi += c[i]*np.cosh((2*i+1)*np.pi*y/L)*np.sin((2*i+1)*np.pi*x/L)

        phiH += 4*h1/((2*i+1)*np.pi) * np.sin((2*i+1)*np.pi*xi/L)


    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    bins = np.arange(h1)+1
    CS = ax.contour(x,y,phi, levels=[1,2,4,6,8,10,12,14,16,18], colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')
    ax.set_xlim(0,L)
    ax.set_ylim(0,H)

    ax.axis('off')

    # ax.set_xlabel('Distance x')
    # ax.set_ylabel('Profondeur y')


    plt.savefig('./figures/Lac2.svg')

    plt.show()

def solution_ecoulement_gauche():

    # Length L, Depth H, Number of terms in the fourier series N
    L=200
    H=100
    N=100

    # Initilize Matrices
    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)
    phi=0*x

    # Non zero BC
    h0=20


    # Initilize fourier constants
    c=np.zeros(N)

    # Loop to calculate Phi
    for i in range(N):
        alpha = (2*i+1)*np.pi/(2*H)
        c[i] = (-1)**(i) * 4* h0/ ((2*i+1) * np.pi * np.sinh(-alpha*L))
        print (2*i+1,c[i])
        phi += c[i]*np.sinh(alpha*(x-L))*np.cos(alpha*y)


    # Calculate velocity (here K=1 m/s)
    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)

    # Plot the result
    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    # bins = np.arange(h0)+1
    CS = ax.contour(x,y,phi, levels=[1,2,4,6,8,10,12,14,16,18], colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')
    ax.set_xlim(0,L)
    ax.set_ylim(0,H)

    ax.set_xlabel('Distance')
    ax.set_ylabel('Depth')

    plt.show()

def solution_ecoulement_droite():

    L=200
    H=100
    N=100

    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)



    phi=0*x

    h2=10

    c=np.zeros(N)


    for i in range(N):
        alpha = (2*i+1)*np.pi/(2*H)
        c[i] = (-1)**(i) * 4* h2/ ((2*i+1) * np.pi * np.sinh(alpha*L))
        print (2*i+1,c[i])
        phi += c[i]*np.sinh(alpha*x)*np.cos(alpha*y)



    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    # bins = np.arange(h0)+1
    CS = ax.contour(x,y,phi, levels=[1,2,4,6,8,10,12,14,16,18], colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')
    ax.set_xlim(0,L)
    ax.set_ylim(0,H)

    # ax.axis('off')


    plt.savefig('./figures/lac_3_ecoulement_droite.pdf')
    plt.show()

def solution_lac3():

    L=200
    H=100
    N=100

    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)



    phi=0*x

    h0=20
    h1=15
    h2=10

    c=np.zeros(N)

    #gauche
    for i in range(N):
        alpha = (2*i+1)*np.pi/(2*H)
        c[i] = (-1)**(i) * 4* h0/ ((2*i+1) * np.pi * np.sinh(-alpha*L))
        print (2*i+1,c[i])
        phi += c[i]*np.sinh(alpha*(x-L))*np.cos(alpha*y)

    #lac
    for i in range(N):
        c[i] = 4*h1/((2*i+1)*np.pi*np.cosh((2*i+1)*np.pi*H/L))
        print (2*i+1,c[i])
        phi += c[i]*np.cosh((2*i+1)*np.pi*y/L)*np.sin((2*i+1)*np.pi*x/L)


    #droite
    for i in range(N):
        alpha = (2*i+1)*np.pi/(2*H)
        c[i] = (-1)**(i) * 4* h2/ ((2*i+1) * np.pi * np.sinh(alpha*L))
        print (2*i+1,c[i])
        phi += c[i]*np.sinh(alpha*x)*np.cos(alpha*y)



    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    bins = np.arange(10)+h2
    CS = ax.contour(x,y,phi, levels=bins, colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')
    ax.set_xlim(0,L)
    ax.set_ylim(0,H)

    ax.axis('off')


    plt.savefig('./figures/lac_3.svg')
    plt.show()

def nterms():

    L=200
    H=100
    N=100
    xi=np.linspace(0,L,100)
    yi=np.linspace(0,H,100)

    x,y = np.meshgrid(xi,yi)

    phi=0*x

    h1=20


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)

    for N in [1,5,10,50,100]:
        phiH=np.zeros(100)
        c=np.zeros(N)
        for i in range(N):
            c[i] = 4*h1/((2*i+1)*np.pi*np.sinh((2*i+1)*np.pi*H/L))
            print (2*i+1,c[i])
            phiH += 4*h1/((2*i+1)*np.pi) * np.sin((2*i+1)*np.pi*xi/L)
        ax.plot(xi,phiH/h1,'-', label=N)

    ax.set_xlabel('distance X')
    ax.set_ylabel('$\phi_{cal}/\phi_{th}$')
    ax.legend(loc='lower center')
    plt.savefig('./figures/convergence_Lac1.pdf',bbox_inches='tight')
    plt.show()


def psi(phi,x,y):

    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)

    print(np.shape(U),np.shape(V))
    f=plt.figure()
    ax=f.add_subplot(111)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],density=0.5)

    # plt.show()



def profil_1D():

    L=2000
    h1=10
    h2=20

    x=np.linspace(0,L)

    phic = (h2-h1)*x/L + h1
    phil = np.sqrt( (h2**2-h1**2)*x/L + h1**2 )

    fig=plt.figure(figsize=(14/2.54,7/2.54))
    plt.plot(x,phic,label=u'Nappe captive')
    plt.plot(x,phil,label='Nappe libre')

    plt.xlabel('Distance x')
    plt.ylabel('Charge')
    plt.legend(loc='lower right')
    # plt.xlim(0,2000)
    # plt.ylim(0,20)

    plt.savefig('./figures/profil1D_com.pdf',bbox_inches='tight')
    plt.show()

def solnum_PL1():

    #################################################################
    #
    # Jacobi iterative method to solve laplace equation with
    # Dirichlet type BCs on a rectangular grid
    #
    #################################################################

    # Grid size
    Nx=50
    Ny=25

    # Coordinates
    xi=np.linspace(0,Nx,Nx)
    yi=np.linspace(0,Ny,Ny)
    x,y = np.meshgrid(xi,yi)
    delta = 1 # dx=dy=1

    #Initialize ptential function
    phi=0*x

    # Boundaries
    # Initialize Boundary matrix B
    Boundary_points = np.zeros((Ny,Nx))

    # Declare boundary points
    # Boundary_points =1 => Boundary
    # Boundary_points =0 => inner point where the laplacian is to be calculated
    Boundary_points[:,0] = 1
    Boundary_points[:,Nx-1] = 1
    Boundary_points[0,:] = 1
    Boundary_points[Ny-1,:] = 1

    # Dirichlet condition on the limits (change accordingly)
    phi[Ny-1,:] = 20
    phi[0,:] = 0
    phi[:,0] = 0
    phi[:,Nx-1] = 0


    #convergence criteria
    epsilon=10
    conv_crit = 0.0005

    #########################################
    # Loop to solve Delta Phi = 0
    #########################################
    while epsilon > conv_crit:
        phi_copy = phi.copy()
        for i in range(Ny):
            for j in range(Nx):
                if Boundary_points[i,j] == 0:
                    phi[i,j] = (phi_copy[i-1,j]+phi_copy[i+1,j]+phi_copy[i,j-1]+phi_copy[i,j+1])/4
            epsilon = np.sqrt(np.matrix((phi-phi_copy)**2).sum()/(Nx*Ny))
        print( epsilon )
    #########################################


    # Calculate velocity vectors
    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    # Plot equipotentials and streamlines
    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    CS = ax.contour(x,y,phi, levels=range(0,20,2), colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)
    ax.axis('square')

    plt.show()

def solnum_PL2():

    #################################################################
    #
    # Jacobi iterative method to solve laplace equation with
    # Dirichlet and Neumann type BCs on a rectangular grid
    #
    #################################################################

    Nx=50
    Ny=25

    xi=np.linspace(0,Nx,Nx)
    yi=np.linspace(0,Ny,Ny)

    delta = 1 # dx=dy=1

    x,y = np.meshgrid(xi,yi)

    #Initialize potential function
    phi=0*x

    # Boundaries
    # Initialize Boundary matrix B
    Boundary_points = np.zeros((Ny,Nx))
    # declare boundary points
    # Boundary_points =1 => Boundary
    # Boundary_points =0 => inner point where the laplacian is to be calculated
    Boundary_points[:,0] = 1
    Boundary_points[:,Nx-1] = 1
    Boundary_points[0,:] = 1
    Boundary_points[Ny-1,:] = 1

    # Dirichlet condition on the upper limits
    phi[Ny-1,:] = 20
    phi[:,0] = 0
    phi[:,Nx-1] = 0
    # Neuman condition flux=0 on the lower limit
    dphi = np.zeros(Nx)


    epsilon=10
    conv_crit = 0.0005

    while epsilon > conv_crit:
        phi_copy = phi.copy()
        for i in range(Ny):
            for j in range(Nx):
                if Boundary_points[i,j] == 0:
                    phi[i,j] = (phi_copy[i-1,j]+phi_copy[i+1,j]+phi_copy[i,j-1]+phi_copy[i,j+1])/4
                # treatment of the Neumann condition on the lower boundary.
                # Beware of the (i,j) inversion with regard to (x,y)
                # i -> y
                # j -> x
                if i==0 and 0 < j < Nx-1:
                    phi[i,j] = phi[i+1,j] + delta * dphi[j]
        epsilon = np.sqrt(np.matrix((phi-phi_copy)**2).sum()/(Nx*Ny))
        print( epsilon )


    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(14/2.54,7/2.54))
    ax = fig.add_subplot(111)
    CS = ax.contour(x,y,phi, levels=range(0,20,2), colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)

    plt.show()

def sol_num_dam():

    #################################################################
    #
    # Jacobi iterative method to solve laplace equation with
    # Dirichlet and Neumann type BCs on a rectangular grid
    # with application to a dam  & all side fluxes are null
    #################################################################

    Nx=75 # 3 squares  of 25x25
    Ny=25

    xi=np.linspace(0,Nx,Nx)
    yi=np.linspace(0,Ny,Ny)

    delta = 1 # dx=dy=1

    x,y = np.meshgrid(xi,yi)

    #Initialize potential function
    phi=0*x

    # Boundaries
    # Initialize Boundary matrix B
    Boundary_points = np.zeros((Ny,Nx))
    # declare boundary points
    # Boundary_points =1 => Boundary
    # Boundary_points =0 => inner point where the laplacian is to be calculated
    Boundary_points[:,0] = 1
    Boundary_points[:,Nx-1] = 1
    Boundary_points[0,:] = 1
    Boundary_points[Ny-1,:] = 1

    # Dirichlet condition on the upper limits
    # there its a bit more complex
    # beware with the initial imposed BCs because it can be very difficult fror the code to converge if they are ill chosen.
    phi[Ny-1,:32] = 30 # upstream lake
    phi[Ny-1,33:74] = 10 # downstream lake


    epsilon=10
    conv_crit = 0.0005

    while epsilon > conv_crit:
        phi_copy = phi.copy()
        for i in range(Ny):
            for j in range(Nx):
                if Boundary_points[i,j] == 0:
                    phi[i,j] = (phi_copy[i-1,j]+phi_copy[i+1,j]+phi_copy[i,j-1]+phi_copy[i,j+1])/4
                # treatment of the Neumann condition on the lower boundary.
                # Beware of the (i,j) inversion with regard to (x,y)
                # i -> y
                # j -> x
                # easiest  the lower BC
                if i==0 and 0 < j < Nx-1:
                    phi[i,j] = phi[i+1,j]
                # upper bc in the middle
                if i==Ny-1 and 25 < j < 49:
                    phi[i,j] = phi[i-1,j]
                # Left Side BC
                if j==0 and 0 < i <Ny-1:
                    phi[i,j] = phi[i,j+1]
                # right BC
                if j==Nx-1 and 0 < i <Ny-1:
                    phi[i,j] = phi[i,j-1]


        epsilon = np.sqrt(np.matrix((phi-phi_copy)**2).sum()/(Nx*Ny))
        print( epsilon )


    U=-np.diff(phi,axis=1)/np.diff(x,axis=1)
    V=-np.diff(phi,axis=0)/np.diff(y,axis=0)


    fig = plt.figure(figsize=(18/2.54,6/2.54))
    ax = fig.add_subplot(111)
    CS = ax.contour(x,y,phi, levels=range(10,30,2), colors='blue')
    ax.clabel(CS, inline=1, fontsize=10)
    ax.streamplot(x[1:,1:],y[1:,1:],U[1:,:],V[:,1:],color='red',density=0.5)

    ax.set_xlim(0,74)
    ax.set_ylim(0,24)
    plt.axis("off")

    plt.savefig("./figures/dam_sol.svg", bbox_inches='tight')
    plt.show()

def grid_sol_num():

    fig = plt.figure(figsize=(10/2.54,10/2.54))
    for i in np.arange(0,10,2):
        for j in np.arange(0,10,2):
            plt.plot([i,i],[-2,10],'k-')
            plt.plot([-2,10],[j,j],'k-')
            plt.plot(i,j,'ko')

    plt.plot(-2*np.ones(5),np.arange(0,10,2),'bs')
    plt.plot(10*np.ones(5),np.arange(0,10,2),'bs')
    plt.plot(np.arange(0,10,2),-2*np.ones(5),'bs')
    plt.plot(np.arange(0,10,2),10*np.ones(5),'bs')

    plt.axis('square')
    plt.axis('off')
    plt.savefig('./figures/grid_num.pdf')

    plt.show()


if __name__ == '__main__':
    # triangulation()
    # laplace_signification()
    #laplace_solution_captive()
    # solution_dupuit_deux_puits()

    solution_lac_0()
    # solution_lac_2()
    # solution_ecoulement_gauche()
    # solution_ecoulement_droite()

    # solution_lac3()

    # profil_1D()

    # solnum_PL1()
    # solnum_PL2()
    # sol_num_dam()
    # grid_sol_num(),'k-'
    # annulus_fig()
    # sol_plateau1S()
    # sol_ile()

    # plt.show()
