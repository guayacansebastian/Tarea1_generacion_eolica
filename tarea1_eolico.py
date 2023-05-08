import matplotlib.pyplot as plt # Esta función es utilizada para mostrar los gráficos
import pandas
import numpy as np
import pandas as pnd
import seaborn as sbn
sbn.set(rc={'figure.figsize':(10, 5)})


class Eolico():

    def __init__(self):
        self.path_met = "datos_met.csv"
        self.path_sitio = "datos_sitio.csv"  
        self.altura = 106 #metros
        self.alpha = 0.198 #coeficiente cortante del viento
        self.vel_int = []
        self.carga_datos()     
        self.extrapolar()
        self.velocidad_promedio()


    def carga_datos (self):
        self.met = open(self.path_met, "r")
        titulos = self.met.readline().split(",")
        linea = self.met.readline().split(",")
        self.datos={
                "FECHA" :[] ,
                "TEMPERATURA":[],
                "HUMEDAD":[],
                "PRESION":[],
                "SPEED60":[],
                "DIR98":[]
            }
        i = 0
        while len(linea[0]) > 0:
            self.datos["FECHA"].append(pnd.to_datetime(  linea[0] + "-" + linea[1] + "-"+ linea[2] + " "+ linea[3] + ":"+ linea[4] ))
            self.datos["TEMPERATURA"].append(float(linea[5]))
            self.datos["HUMEDAD"].append(float(linea[6]))
            self.datos["PRESION"].append(float(linea[7].replace("\n", "")))
            linea = self.met.readline().split(",")
        self.sitio = open(self.path_sitio, "r")
        linea = self.sitio.readline().split(",")
        linea = self.sitio.readline().split(",")
        while len(linea[0]) > 0:
            self.datos["SPEED60"].append(float(linea[5]))
            self.datos["DIR98"].append(float(linea[6].replace("\n","")))        
            linea = self.sitio.readline().split(",")


    def extrapolar(self):
        for i in range(len(self.datos["SPEED60"])):
            v =  float (self.datos["SPEED60"][i]* (106/60)**(self.alpha ))
            self.vel_int.append(v)
        time = self.datos["FECHA"]
        plt.figure()
        plt.plot( time,self.datos["SPEED60"],label='60m')
        plt.plot( time,self.vel_int,label='106m')
        plt.title("Velocidad del viento extrapolada a 106m")
        plt.xlabel("Fecha")
        plt.ylabel("Velocidad del viento (m/s)")
        plt.legend()

        
    def velocidad_promedio(self):
        prom = {}
        for i in range(len (self.vel_int)):
            año = self.datos["FECHA"][i].year
            mes = self.datos["FECHA"][i].month
            if año not in prom:
                prom[año]={}
                prom[año][mes] = self.vel_int[i]
            else:
                if mes not in prom[año]:
                    prom[año][mes] = self.vel_int[i]
                else : 
                    prom[año][mes] += self.vel_int[i]
        key1 = list(prom.keys())
        vel_prom =[]
        for i in range(len(key1)):
            lista = []
            key2 =  list (prom[key1[i]].keys())
            for j in range(len(key2)):
                promedio_mes= prom[key1[i]][key2[j]] / 730
                lista.append(promedio_mes)
            vel_prom.append(lista)
        prom_total = []
        for i in range(len(vel_prom[0])):
            mes = 0
            for j in range(len(vel_prom)):
                mes += vel_prom[j][i]
            mes = mes /10
            prom_total.append(mes)
        plt.figure()
        plt.plot( prom_total,"o" ,label='Promedio 10 años')
        plt.plot( vel_prom[0],label='2008')
        plt.plot( vel_prom[1],label='2009')
        plt.plot( vel_prom[2],label='2010')
        plt.plot( vel_prom[3],label='2011')
        plt.plot( vel_prom[4],label='2012')
        plt.plot( vel_prom[5],label='2013')
        plt.plot( vel_prom[6],label='2014')
        plt.plot( vel_prom[7],label='2015')
        plt.plot( vel_prom[8],label='2016')
        plt.plot( vel_prom[9],label='2017')
        plt.title("Velocidad  Promedio del viento extrapolada a 106m")
        plt.xlabel("Mes ")
        plt.ylabel("Velocidad del viento (m/s)")
        plt.legend(loc='lower left')
        plt.show()


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
