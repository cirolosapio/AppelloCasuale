import random
import os
import pandas as pd

class AppelloCasuale:
    def __init__(self, classe=None):
        self.classe = classe
        self.appello_corrente = list()
        self.indice_attuale = 0
        self.path = ''

    def chiamare_ragazzo(self):
        if self.indice_attuale == len(self.appello_corrente):
            print("------------------Sono stati chiamati tutti-------------------")
            self.set_classe(self.path, self.classe)
            

        ragazzo_chiamato = self.appello_corrente[self.indice_attuale]
        self.indice_attuale += 1
        return ragazzo_chiamato[0].upper() + ' ' +  ragazzo_chiamato[1].upper() #nome + cognome

    def set_classe(self, class_path, classe):
        self.path = class_path
        df = pd.read_excel(os.path.join(class_path, classe), sheet_name='Foglio1')
        data_array = df.to_numpy()
        self.classe = classe
        self.appello_corrente = list(data_array)
        random.shuffle(self.appello_corrente)
        self.indice_attuale = 0

    def get_classe(self):
        return self.classe