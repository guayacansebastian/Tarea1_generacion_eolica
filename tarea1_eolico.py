import matplotlib as mt
import pandas
import numpy as np




class Eolico():

    def __init__(self):
        self.path_met = "datos_met.csv"
        self.path_sitio = "datos_sitio.csv"  

        self.carga_datos()     
        pass 
    def carga_datos (self):
        self.met = open(self.path_met, "r")
        titulos = self.met.readline().split(",")
        linea = self.met.readline().split(",")
        self.datos=[]
        while len(linea[0]) > 0:
            dicc = {
                "YEAR":linea[0],
                "MES":linea[1],
                "DIA":linea[2],
                "HORA":linea[3],
                "MINUTO":linea[4],
                "TEMPERATURA":linea[5],
                "HUMEDAD":linea[6],
                "PRESION":linea[7].replace("\n", "")
            }
            self.datos.append(dicc)
            linea = self.met.readline().split(",")
        self.sitio = open(self.path_sitio, "r").readlines()
    
        for i in range(len(self.datos)-1):
            linea = self.sitio[i+1].split(",")
            self.datos[i]["SPEED60"]=linea[5]
            self.datos[i]["DIR98"]=linea[6].replace("\n","")

        print ((self.datos[0]))

        pass
    def extrapolar(self):
        pass
    def velocidad_promedio(self):
        pass
    def patron_anual(self):
        pass
    def param_weibull(self):
        pass
    def distr_weibull(self):
        pass
    def rosa_vientos(self):
        pass

def main(args=None):
    tarea1 = Eolico()


if __name__ == '__main__':
    main()
