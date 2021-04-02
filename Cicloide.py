import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt


class Cicloide():
    """La classe cicloide calcula l'equació de la cilcoide per cert num de punts"""
    def __init__(self, p2):

        #Usem Newton-Raphson per trobar theta
        f = lambda theta: -p2[1] / p2[0] - (1 - np.cos(theta)) / (theta - np.sin(theta))
        theta = newton(f, np.pi / 2)

        # A partir de theta calculem el radi
        R = -p2[1] / (1 - np.cos(theta))

        #Per la propietat taurocrona de la braquistrocona
        self.temps = np.pi * np.sqrt(R/9.8)

        xs = np.linspace(0, 3.50, 1000)

        x = R * (xs - np.sin(xs))
        y = R * (1 - np.cos(xs))

        plt.plot(x, -y, 'k', lw=3, label="Cicloide")