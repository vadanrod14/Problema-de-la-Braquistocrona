from Cicloide import Cicloide
from Cromosoma import Cromosoma
import operator
from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class Poblacio():
    """La classe població emmagatzema els elements
    de la població"""

    def __init__(self, num_individus, num_punts, prob_mutacio):

        self.num_individus = num_individus
        self.num_punts = num_punts
        self.prob_mutacio = prob_mutacio

        #Crea individus
        self.poblacio = [Cromosoma(num_punts, (0, 0), (2, -1)) for i in range(self.num_individus)]
        self.cicloide = Cicloide((2, -1))

    def ordena_poblacio(self):
        '''Ordena la població segons el temps de menor a major'''
        self.poblacio = sorted(self.poblacio, key=operator.attrgetter("temps"))
        self.millor = self.poblacio[0].temps
        llista_temps = [indiv.temps for indiv in self.poblacio]
        self.mitjana = sum(llista_temps)/ len(llista_temps)

    def mutacio(self):
        '''Donat una constant de probabilitat de mutacio, s'intercanvien posisició (es a dir, valors d'y)
        ara amb probabilitat 1/num_punts'''
        for i in range(len(self.poblacio)):
            if random() < self.prob_mutacio:
                for j in range(1, self.num_punts - 1):
                    if random() < 1/len(self.poblacio):
                        # self.poblacio[i].y[j], self.poblacio[i].y[j-1] = self.poblacio[i].y[j-1], self.poblacio[i].y[j]
                        self.poblacio[i].y[j] = np.random.uniform(self.poblacio[i].y[j] - 1/100, self.poblacio[i].y[j] + 1/100)
                        # self.poblacio[i].y[j] = np.random.uniform(-1, -self.poblacio[i].x[j]/2)

                self.poblacio[i].calcula_temps()

    def encreuaments(self):
        '''Donada una prob que decreix segons la posició a la llista va abaixant, i un punt d'encreuament
        també pres de forma aleatoria, s'encreuen dues corbes'''

        index_indiv_0 = -1
        cont = 1
        for i in range(len(self.poblacio)):
            if random() < ((1 - i/self.num_individus) - 0.40):
                if index_indiv_0 != -1:
                    # punt_tall = randint(0, self.num_punts)
                    punt_tall = 5
                    self.poblacio[len(self.poblacio) - cont].y = self.poblacio[index_indiv_0].y[:punt_tall] + self.poblacio[i].y[punt_tall:]
                    self.poblacio[len(self.poblacio) - cont - 1].y = self.poblacio[i].y[:punt_tall] + self.poblacio[index_indiv_0].y[punt_tall:]
                    self.poblacio[len(self.poblacio) - cont].calcula_temps(), self.poblacio[len(self.poblacio) - cont - 1].calcula_temps()
                    index_indiv_0 = -1
                    cont += 1
                else:
                    index_indiv_0 = i

    def descarta_repetits(self):
        remove_ = []
        for i in range(self.num_individus):
            for j in range(i+1, self.num_individus -1):
                if abs(self.poblacio[i].temps - self.poblacio[j].temps) < 0.00001:
                    remove_.append(self.poblacio[i])
        poblacio = []
        for indiv in self.poblacio:
            if indiv not in self.poblacio:
                poblacio.append(indiv)
        self.poblacio = poblacio

    def afegeix_nous_indiv(self):
        for i in range(len(self.poblacio) + 1, self.num_individus):
            self.poblacio.append(Cromosoma(self.num_punts, (0, 0), (2, -1)))
            # self.poblacio[-1].y = self.poblacio[0].y
            for j in range(2, self.num_punts - 1):
                self.poblacio[-1].y[j] = np.random.uniform(self.poblacio[0].y[j] - 1 / 100,
                                                              self.poblacio[0].y[j] + 1 / 100)
            self.poblacio[-1].calcula_temps()

    def dibuixa_corbes(self, gen):
        xs = np.linspace(0, 2, 1000)
        plt.plot(xs, self.poblacio[0].f(xs), lw=3, linewidth=2, label="gen: " + str(gen))
        plt.legend()
        plt.savefig("Imatges/Image_" + str(gen) + ".png")

p = Poblacio(num_individus=10, num_punts=10, prob_mutacio=0.50)
num_generacions = 10000
millor = []
mitja = []
for k in range(num_generacions):
    p.ordena_poblacio()
    if k % 10 == 0:
        print("Gen: " + str(k) + " Millor corba: " + str(p.millor)[0:8] + ", Mitja: " + str(p.mitjana)[:8] + ", Cicloide " + str(p.cicloide.temps)[0:8])
        millor.append(p.millor - p.cicloide.temps)
        mitja.append(p.mitjana - p.cicloide.temps)
    if k % 200 == 0:
        p.dibuixa_corbes(k)
        print(millor)
        print(mitja)
    p.mutacio()
    p.encreuaments()
    # p.descarta_repetits()
    # p.afegeix_nous_indiv()

print(p)

