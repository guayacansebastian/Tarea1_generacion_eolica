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
        self.vel_promedio_total = 0
        self.st_dev = 0
        self.k=0
        self.lammbda = 0
        self.vel_int = []
        self.prom_mes = {}
        self.prom_hora = {}
        self.prom_total_mes = []
        self.prom_total_hora = []
        self.carga_datos()     
        self.extrapolar()
        self.velocidad_promedio()
        self.patron_anual()
        self.param_weibull()
        self.distr_weibull()
        self.rosa_vientos()


    def carga_datos (self):
        self.met = open(self.path_met, "r")
        self.met.readline().split(",")
        linea = self.met.readline().split(",")
        self.datos={
                "FECHA" :[] ,
                "TEMPERATURA":[],
                "HUMEDAD":[],
                "PRESION":[],
                "SPEED60":[],
                "DIR98":[],
                "DIR_DEG":[]
            }
        i = 0
        while len(linea[0]) > 0:
            self.datos["FECHA"].append(pnd.to_datetime(  linea[0] + "-" + linea[1] + "-"+ linea[2] + " "+ linea[3] + ":"+ linea[4] ))
            self.datos["TEMPERATURA"].append(float(linea[5]))
            self.datos["HUMEDAD"].append(float(linea[6]))
            self.datos["PRESION"].append(float(linea[7].replace("\n", "")))
            linea = self.met.readline().split(",")
        self.sitio = open(self.path_sitio, "r")
        self.sitio.readline().split(",")
        linea = self.sitio.readline().split(",")
        while len(linea[0]) > 0:
            self.datos["SPEED60"].append(float(linea[5]))
            dir = (float(linea[6].replace("\n",""))*np.pi / 180)
            self.datos["DIR98"].append(round(dir,1) )        
            self.datos["DIR_DEG"].append(float(linea[6].replace("\n","")))        
            #self.datos["DIR98"].append(np.deg2rad(float(linea[6].replace("\n","")) ))        
            

            linea = self.sitio.readline().split(",")


    def extrapolar(self):
        for i in range(len(self.datos["SPEED60"])):
            v =  float (self.datos["SPEED60"][i]* (106/60)**(self.alpha ))
            self.vel_int.append(v)
        time = self.datos["FECHA"]
        plt.figure(1)
        plt.plot( time,self.datos["SPEED60"],label='60m')
        plt.plot( time,self.vel_int,label='106m')
        plt.title("Velocidad del viento extrapolada a 106m")
        plt.xlabel("Año")
        plt.ylabel("Velocidad del viento (m/s)")
        plt.legend()

        
    def velocidad_promedio(self):
        
        for i in range(len (self.vel_int)):
            año = self.datos["FECHA"][i].year
            mes = self.datos["FECHA"][i].month
            if año not in self.prom_mes:
                self.prom_mes[año]={}
                self.prom_mes[año][mes] = self.vel_int[i]
            else:
                if mes not in self.prom_mes[año]:
                    self.prom_mes[año][mes] = self.vel_int[i]
                else : 
                    self.prom_mes[año][mes] += self.vel_int[i]
        key1 = list(self.prom_mes.keys())
        vel_prom =[]
        for i in range(len(key1)):
            lista = []
            key2 =  list (self.prom_mes[key1[i]].keys())
            for j in range(len(key2)):
                promedio_mes= self.prom_mes[key1[i]][key2[j]] / 730
                lista.append(promedio_mes)
            vel_prom.append(lista)
        
        for i in range(len(vel_prom[0])):
            mes = 0
            for j in range(len(vel_prom)):
                mes += vel_prom[j][i]
            mes = mes /10
            self.prom_total_mes.append(mes)
        plt.figure(2)
        plt.plot( self.prom_total_mes,"o-" ,label='Promedio 10 años')
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
        plt.title("Velocidad  promedio mensual del viento  a 106m")
        plt.xlabel("Mes ")
        plt.ylabel("Velocidad del viento (m/s)")
        plt.legend(loc='lower left')


    def patron_anual(self):
        
        for i in range(len (self.vel_int)):
            año = self.datos["FECHA"][i].year
            hora = self.datos["FECHA"][i].hour
            if año not in self.prom_hora:
                self.prom_hora[año]={}
                self.prom_hora[año][hora] = self.vel_int[i]
            else:
                if hora not in self.prom_hora[año]:
                    self.prom_hora[año][hora] = self.vel_int[i]
                else : 
                    self.prom_hora[año][hora] += self.vel_int[i]
        key1 = list(self.prom_hora.keys())
        vel_prom =[]
        for i in range(len(key1)):
            lista = []
            key2 =  list (self.prom_hora[key1[i]].keys())
            for j in range(len(key2)):
                promedio_hora= self.prom_hora[key1[i]][key2[j]] / 365
                lista.append(promedio_hora)
            vel_prom.append(lista)
        
        for i in range(len(vel_prom[0])):
            hora = 0
            for j in range(len(vel_prom)):
                hora += vel_prom[j][i]
            hora = hora /10
            self.prom_total_hora.append(hora)
        plt.figure(3)
        plt.plot( self.prom_total_hora,"o-" ,label='Promedio 10 años')
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
        plt.title("Velocidad  promedio diaria del viento a 106m")
        plt.xlabel("Hora ")
        plt.ylabel("Velocidad del viento (m/s)")
        plt.legend(loc='upper right')
        #plt.show()


    def param_weibull(self):
        suma = 0
        for i in range( len(self.prom_total_mes) ):
            suma += self.prom_total_mes[i]
        self.vel_promedio_total= suma/12
        print (f"Velocidad promedio total = {self.vel_promedio_total}")
        self.st_dev = np.std(np.array(self.vel_int)  )
        print("Desviación estándar: " + str(self.st_dev))
        self.k= (self.st_dev/ self.vel_promedio_total)**(-1.086)
        print("k: " + str(self.k))
        self.lammbda = self.vel_promedio_total*(0.568 + (0.433/self.k))**(-1/self.k)
        print("lambda: " + str(self.lammbda))

        
    def distr_weibull(self):
        x_hist = np.arange(0, 10, 0.2)
        y_hist = []
        for i in range(len (self.datos["SPEED60"])):
            vel = self.datos["SPEED60"][i]
            for j in range(len (x_hist)-1):
                if vel < x_hist[j+1] and vel > x_hist[j]:
                    y_hist.append(x_hist[j])
        x = np.arange(0, 10, 0.01)
        weibull = []
        for i in range(len(x)):
            w = ((self.k/self.lammbda)*(x[i]/self.lammbda)**(self.k-1) )*(np.exp(-(x[i]/self.lammbda)**(self.k)))
            weibull.append(w*100)
        fig, axs = plt.subplots(2)
        fig.suptitle('Velocidad del viento')     
        axs[0].plot( x,weibull,"tab:red",label = "Weibull")
        axs[0].legend(loc='upper right')
        axs[0].set_ylabel("%")
        axs[0].set_xlabel("Velocidad viento (m/s) ")
        axs[1].hist( y_hist,bins=100, label = "Histograma")
        axs[1].legend(loc='upper right')
        axs[1].set_ylabel("Número de horas - total")
        axs[1].set_xlabel("Velocidad viento (m/s) ")
        


    def rosa_vientos(self):
        theta = {}
        r = []
        angs = []
        for i in range(len (self.vel_int)):
            dir = self.datos["DIR98"][i]
            if dir not in theta:
                ans = [self.vel_int[i],1]
                theta[dir]= ans
                angs.append(dir)
            else:
                theta[dir][0]+= self.vel_int[i]
                theta[dir][1]+= 1
                
        
        angs.sort()
            

        for th in angs:
            pr = theta[th][0] / theta[th][1]
            r.append(pr)
        print (angs)
        #print (f"angs {angs} ")

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(angs, r)
        ax.set_rticks( np.arange(0, 10, 1.5))  # Less radial ticks
        ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        ax.grid(True)
        ax.set_title("Velocidad promedio por dirección", va='bottom')
        plt.show()

        



def main(args=None):
    tarea1 = Eolico()


if __name__ == '__main__':
    main()

