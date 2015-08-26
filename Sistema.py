#Algoritmo y estructura de datos
#Daniela I. Pocasangre A. - 14162
#Juan Diego Benitez C. - 14124
#Este programa simula la corrida de programas dentro de un sistema operativo
#que contiene acciones como New, Ready, Running, Waiting y Terminated

import simpy
from simpy.events import Interrupt
from random import randint
import random
import matplotlib.pyplot as plt


def procesando(env, name, instrucciones, veces): #running
    contador = veces
    totalinstrucciones = instrucciones
    print "Se estan procesando instrucciones del proceso %s" % name
    while contador < veces: #se realizan solo "veces" instrucciones por vez
        if totalinstrucciones > 0:
            contador = contador + 1
            totalintrucciones = totalinstrucciones - 1
            yield env.timeout(5)
        else:
            contador = 4
            yield env.timeout(5)
        yield env.timeout(5)
        
        
def setmemoria(env, name, memoria):
    global totalProcesos
    print "El proceso #%s llega a recibir memoria\n" % name
    with RAMdisponibles.request() as req:
        if RAM.level <= 0:
            yield req
            
        yield RAM.get(memoria) #ready con memoria asignada

def generadorProcesos(env, cantprocesos, intervalo, veces): #new process
    global instrucciones
    for i in range(cantprocesos+1):
        tiempogenerar = random.expovariate(1.0/intervalo)
        memoria = random.randint(1,10) #cant de memoria a usar
        instrucciones = random.randint(1,10) #cant de instrucciones a procesar
        env.process(setmemoria(env,i,memoria))
        llegada = env.now
        print "\nEl proceso #%s acaba de entrar al sistema" % i
        env.process(proceso(i, env, memoria, instrucciones, veces, llegada))
        yield env.timeout(tiempogenerar)

def proceso(name, env, memoria, instrucciones, veces, llegatoria):
    llegada = llegatoria
    global TiempoTotal
    #Valores[1:cantprocesos]
        #ready
    if instrucciones>0:
        with InstruccionesDisponibles.request() as req:
            yield req
            if instrucciones>0:
                env.process(procesando(env, name, instrucciones, veces))
                instrucciones = instrucciones - veces
                yield env.timeout(5)
                #waiting o ready again
                if instrucciones>0: #lo hace si aun quedan instrucciones
                    waiting = random.randint(1,2)
                    if waiting == 1: #waiting
                        print "El proceso %s se encuentra reaizando operaciones de I/O " % name
                        yield env.timeout(7) #hacemos un delay de 7 unidades
                        env.process(proceso(name, env, memoria, instrucciones, veces, llegada))
                    if waiting == 2: #ready again
                        print "El proceso #%s se encuentra esperando a ser atendido de nuevo" % name
                        env.process(proceso(name, env, memoria, instrucciones, veces, llegada))
                else: #Prueba de que si ya no hay instrucciones/terminated
                    
                    #terminated
                    totalProcesos = env.now - llegada #Tiempo que se tarda el proceso en el sistema
                    Valores.append(totalProcesos)
                    print "El proceso #%s salio del sistema.\nEste se tardo %s \n" % (name, totalProcesos)
                    TiempoTotal = TiempoTotal + totalProcesos #Tiempo total de todos los procesos
                    yield RAM.put(memoria) #Regresamos la memoria utilizada
 

env = simpy.Environment() #se crea ambiente
RAMdisponibles = simpy.Resource(env, capacity=1)
InstruccionesDisponibles = simpy.Resource(env, capacity=1)
RAM = simpy.Container(env, init=30, capacity=30)

global Valores
Valores = []
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
veces = 3
TiempoTotal = 0.0
intervalo = 5 #intervalo al que se realizara random de memoria
cantprocesos = 200 #cantidad de procesos a realizar SO
genProcesos = env.process(generadorProcesos(env, cantprocesos, intervalo, veces)) #generan procesos
env.run()

promedio = TiempoTotal/cantprocesos
desvesta = 0
ValorCuadrado = 0
ValoresCuadrados = 0
AdentroRaiz = 0

print "Tiempo Total: %s, cantidad de procesos: %s" % (TiempoTotal, cantprocesos)
print "El tiempo promedio del programa es de %s" % (promedio)
for x in range (cantprocesos):
    ValorCuadrado = Valores[x] * Valores[x]
    ValoresCuadrados = ValoresCuadrados + ValorCuadrado
    AdentroRaiz = ValoresCuadrados/cantprocesos

desvesta = AdentroRaiz**0.5
print "Devesta = %s" % (desvesta)


plt.plot(Valores)
plt.xlabel("Procesos")
plt.ylabel("Tiempo")
plt.show()
