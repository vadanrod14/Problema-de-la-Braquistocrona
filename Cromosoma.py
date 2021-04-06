import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.integrate import quad



class Cromosoma():

    def __init__(self, num_punts, p1, p2):


        #Definim els punts pels cuals es construeix el camí
        self.p1 = p1
        self.p2 = p2

        self.num_punts = num_punts
        self.x = np.linspace(self.p1[0], self.p2[0], num_punts)

        #Omplim y
        self.y = [self.p1[1]]
        for i in range(num_punts - 2):
            self.y.append(np.random.uniform(-1, -self.x[i]/p2[0]))
        self.y.append(self.p2[1])

        self.calcula_temps()

    def calcula_temps(self):

        #Calcul temps des de que deixem caure la particula fins arribar al final
        def funcio_de_cost(x):
            a = np.sqrt(1 + self.f.derivative()(x)**2)/np.sqrt(2*9.8*abs(self.f(x)))
            return a

        # Interpola per crear la funció
        self.f = UnivariateSpline(self.x, self.y, k=4, s=0)
        self.temps = quad(funcio_de_cost, a=self.p1[0], b=self.p2[0])[0]


