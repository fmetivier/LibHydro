"""

Game of wells. 
confined to be adapted for unconfined (change phi -> phi^2)

"""

import numpy as np
import matplotlib.pyplot as plt


def nappe_captive_1D(x, h1, h2, x1, x2):

    a = (h1 - h2) / (x1 - x2)
    b = h1

    phi = a * x + b

    return phi


def nappe_captive(x=0, K=1e-5, D=10, hmin=0, hmax=10):

    phi = nappe_captive_1D(x, hmin, hmax, xmin, xmax)

    uy, ux = np.gradient(-K * phi)

    Q = np.abs(ux * (ymax - ymin) + uy * (xmax - xmin))
    print("Q = ", Q[0, 0])
    return phi, ux, uy, Q


def add_puits_captif_phi(xo, yo, x, y, r_p, phi_p, r_a, phi_a, K):

    rp = r_p * np.ones(np.shape(x))
    ra = r_a * np.ones(np.shape(x))

    radius = np.sqrt(((x - xo) ** 2 + (y - yo) ** 2))

    # remplace 0 par le rayon du puits
    mask = radius == 0
    r = np.copy(radius)
    r[mask] = rp[mask]

    mask = r > r_a
    r2 = np.copy(r)
    r2[mask] = ra[mask]

    phi = ((phi_a - phi_p) / np.log(r_a / r_p)) * np.log(r2) + (
        phi_p * np.log(r_a) - phi_a * np.log(r_p)
    ) / (np.log(r_a / r_p))
    Q = (phi_a - phi_p) / np.log(r_a / r_p) * 2 * np.pi * K

    return phi, Q, (phi_a - phi_p) / np.log(r_a / r_p)


if __name__ == "__main__":

    # grille
    xmin = -200
    xmax = 200
    ymin = -200
    ymax = 200
    step = 1

    X = np.arange(xmin, xmax, step)
    Y = np.arange(ymin, ymax, step)

    x, y = np.meshgrid(X, Y)

    # paramètres de la nappe
    K = 1e-5
    D = 10
    hmin = 0
    hmax = 2

    # génère la nappe captive
    phi, ux, uy, Q = nappe_captive(x, K, D, hmin, hmax)

    fig_cap = plt.figure()
    ax = fig_cap.add_subplot(111)
    c = ax.contour(x, y, phi, 10, colors="C0")
    # ax.clabel(c, inline=1, fontsize=10)
    ax.streamplot(x[1:, :], y[:, 1:], ux, uy, color="C3")
    ax.axis("square")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # plt.savefig("./figures/nc.pdf",bbox_inches='tight')

    pos = [[-50,0],[50,0]]
    # puits
    r_p = 0.5
    h_p = [0, 1]
    r_a = 100
    h_a = [1, 0]

    for i in range(len(pos)):
        p=pos[i]
    # génère un puits
        phi_p, Q_p, a = add_puits_captif_phi(p[0],p[1], x, y, r_p, h_p[i], r_a, h_a[i], K)
        print("Q_p =", Q_p)

        # somme puits + nappe captive
        phi += phi_p

    
    uy_p, ux_p = np.gradient(-K * phi_p)

    # fig_puits = plt.figure()
    # ax = fig_puits.add_subplot(111)
    # c = ax.contour(x, y, phi_p, 20, colors="blue")
    # ax.clabel(c, inline=1, fontsize=10)
    # ax.streamplot(x, y, ux_p, uy_p, color="red")
    #
    # ax.axis("square")

    lines = np.arange(int(np.amin(phi)), int(np.amax(phi)), 1)
    uy, ux = np.gradient(phi)
    fig_pn = plt.figure()
    ax = fig_pn.add_subplot(111)
    c = ax.contour(x, y, phi, 20, colors="C0", linewidth=0.5)
    # ax.clabel(c, inline=2, fontsize=10, fmt="%i")
    ax.streamplot(x, y, -ux, -uy, color="C3", linewidth=0.5)

    theta = np.linspace(np.pi-0.01,0, 200)
    r  = a*(np.pi-theta)*xmax/np.sin(theta)
    
    xlpe = r*np.cos(theta)
    ylpe = r*np.sin(theta)

    for i in range(len(xlpe)):
         if r[i] < r_a: 
             ylpe_max = ylpe[i]
         else:
            ylpe[i] = ylpe_max


    # ax.plot(xlpe[1:], ylpe[1:] ,'-', color='C2')
    # ax.plot(xlpe[1:], -ylpe[1:] ,'-', color='C2')
    # ax.plot(r_a*np.cos(theta), r_a*np.sin(theta),'--', color='C1')
    # ax.plot(r_a*np.cos(theta), - r_a*np.sin(theta),'--', color='C1')


    ax.axis("square")
    ax.set_xlabel("x-distance m")
    ax.set_ylabel("y-distance m")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fname = "./figures/deux_puits_nc_ra_lpe_2.pdf"
    plt.savefig(fname, bbox_inches="tight")

    plt.show()
