"""

Game of wells. 
For confined wells to be adapted for unconfined (change phi -> phi^2)
F.M.

"""

import numpy as np
import matplotlib.pyplot as plt


def nappe_captive_1D(x, h1, h2, x1, x2):
    """Créé une nappe captive 1D, peut être utilisé en 2D pour un champs ne variant que dans la direction des x

    Parameters
    ----------
    x : array 
        1D ou 2D suivant le type de nappe
    h1 : float
        charge en x1
    h2 : float
        charge en x2
    x1 : float
        position 1
    x2 : float
        position 2

    Returns
    -------
    array
        vecteur ou matrice de charge
    """

    a = (h1 - h2) / (x1 - x2)
    b = h1

    phi = a * x + b

    return phi


def nappe_captive(x=0, K=1e-5, D=10, hmin=0, hmax=10):
    """créé une nappe captive 2D à écoulement uniforme dans une seule direction

    Parameters
    ----------
    x : array
        matrice des x, by default 0
    K : float, optional
        conductivité hydraulique, by default 1e-5
    D : float, optional
        profondeur de l'aquifère, by default 10
    hmin : float, optional
        charge min, by default 0
    hmax : float, optional
        charge max, by default 10

    Returns
    -------
    _type_
        _description_
    """

    lx, ly = np.shape(x)
    xmin = x[0,0]
    xmax = x[lx-1,ly-1]

    phi = nappe_captive_1D(x, hmin, hmax, xmin, xmax)

    uy, ux = np.gradient(-K * phi)

    Q = np.abs(ux * (ymax - ymin) + uy * (xmax - xmin))
    print("Q = ", Q[0, 0])
    return phi, ux, uy, Q


def add_puits_captif_phi(xo, yo, x, y, r_p, phi_p, r_a, phi_a, K):
    """ ajoute un puits captif à une nappe sttaique de charge phi_a

    Parameters
    ----------
    xo : float
        x puits
    yo : float
        y puits
    x : array
        matrice des x
    y : array
        matrice des y
    r_p : float
        rayon du puits
    phi_p : float
        charge du puits
    r_a : float
        rayon d'action (de l'anneau externe)
    phi_a : float
        charge au rayon d'action
    K : float
        conductivité hydraulique

    Returns
    -------
    array, float, float
        charge, débit, préfacteur de la solution
    """

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

    ################################################
    #
    # Exemple de deux puits alignés pompant le même 
    # débit dans une nappe statique
    #
    ################################################

    #
    # grille
    #
    xmin = -200
    xmax = 200
    ymin = -200
    ymax = 200
    step = 1

    X = np.arange(xmin, xmax, step)
    Y = np.arange(ymin, ymax, step)

    x, y = np.meshgrid(X, Y)
    print(min(x[:,0]), min(x[0,:]), x[0,0], np.shape(x), x[399,399])

    #
    # paramètres de la nappe
    #
    K = 1e-5 
    D = 10
    hmin = 0
    hmax = 0

    #
    # génère la nappe captive
    #
    phi, ux, uy, Q = nappe_captive(x, K, D, hmin, hmax)

    fig_cap = plt.figure()
    ax = fig_cap.add_subplot(111)
    c = ax.contour(x, y, phi, 10, colors="C0")
    ax.streamplot(x[1:, :], y[:, 1:], ux, uy, color="C3")
    ax.axis("square")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    #
    # ajout des puits
    #
    pos = [[-50,0],[50,0]]
    r_p = 0.5
    h_p = [0, 0]
    r_a = 100
    h_a = [1, 1]

    for i in range(len(pos)):
        p=pos[i]
        # génère les puits
        phi_p, Q_p, a = add_puits_captif_phi(p[0],p[1], x, y, r_p, h_p[i], r_a, h_a[i], K)
        print("Q_p =", Q_p)
        print("a =", a)

        # somme les puits et la nappe captive
        phi += phi_p

    
    uy_p, ux_p = np.gradient(-K * phi_p)

    #
    # Figure
    #
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


    ax.axis("square")
    ax.set_xlabel("x-distance m")
    ax.set_ylabel("y-distance m")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fname = "puits_exemple.pdf"
    plt.savefig(fname, bbox_inches="tight")

    plt.show()
