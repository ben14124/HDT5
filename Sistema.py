#Algoritmo y estructura de datos
#Daniela I. Pocasangre A. - 14162
#Juan Diego Benitez C. - 14124
#Este programa simula la corrida de programas dentro de un sistema operativo
#que contiene acciones como New, Ready, Running, Waiting y Terminated

import simpy
from random import randint
import random

class SistemaOperar:
    def __init__(self, env):
        self.RAMdisponibles = simpy.Resource(env, capacity=1)
        self.InstruccionesDisponibles = simpy.Resource(env, capacity=1)
        self.RAM = simpy.Container(env, init=30, capacity=30)
        self.monitoreo = env.process(self.monitor_memory(env))

    def monitor_memory(self, env):
        while True:
            if self.RAM.level <= 0:
                print "No hay suficiente memoria. Se debe de esperar"
            yield env.timeout(5)

def procesando(env, name, instrucciones, veces): #running - arreglar logica
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

def proceso(name, env, SistemaO, memoria, instrucciones, veces, llegatoria):
    llegada = llegatoria
    global TiempoTotal
        #ready
    if instrucciones>0:
        with SistemaO.InstruccionesDisponibles.request() as req:
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
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones, veces, llegada))
                    if waiting == 2: #ready again
                        print "El proceso #%s se encuentra esperando a ser atendido de nuevo" % name
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones, veces, llegada))
                else: #Prueba de que si ya no hay instrucciones/terminated
                    yield SistemaO.RAM.put(memoria)
                    #terminated
                    totalProcesos = env.now - llegada #Tiempo que se tarda el proceso en el sistema
                    print "El proceso #%s salio del sistema.\nEste se tardo %s \n" % (name, totalProcesos)
                    TiempoTotal = TiempoTotal + totalProcesos #Tiempo total de todos los procesos

def setmemoria(env, name, memoria):
    global totalProcesos
    #global llegada
    #llegada = env.now #Se registra el tiempo en el que el proeceso llego al sistema
    print "El proceso #%s llega a recibir memoria\n" % name
    with SistemaO.RAMdisponibles.request() as req:
        if SistemaO.RAM.level <= 0:
            yield req
            
        yield SistemaO.RAM.get(memoria) #ready con memoria asignada

def generadorProcesos(env, SistemaO, cantprocesos, intervalo, veces): #new process
    global instrucciones
    #global TiempoTotal
    #TiempoTotal = 0.0
    tiempogenerar = random.expovariate(1.0/intervalo)
    for i in range(cantprocesos+1):
        memoria = random.randint(1,10) #cant de memoria a usar
        instrucciones = random.randint(1,10) #cant de instrucciones a procesar
        env.process(setmemoria(env,i,memoria))
        llegada = env.now
        print "\nEl proceso #%s acaba de entrar al sistema" % i
        env.process(proceso(i, env, SistemaO, memoria, instrucciones, veces, llegada))
        yield env.timeout(tiempogenerar)

env = simpy.Environment() #se crea ambiente
SistemaO = SistemaOperar(env) #instancia objeto de sistema operativo 
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
veces = 3
TiempoTotal = 0.0
intervalo = 10 #intervalo al que se realizara random de memoria
cantprocesos = 11 #cantidad de procesos a realizar SO
genProcesos = env.process(generadorProcesos(env, SistemaO, cantprocesos, intervalo, veces)) #generan procesos
env.run(300)
promedio = TiempoTotal/cantprocesos
print "El tiempo promedio del programa es de %s" % (promedio)
