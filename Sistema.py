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

    def monitor_memory(self,env):
        while True:
            print "---.--- monitor_memory"
            if self.RAM.level <= 0:
                print('El proceso %s al llegar en %s esta esperando...' % (env.now)) #aqui se aplica el waiting
            yield env.timeout(5)

def procesando(env, name, instrucciones, veces): #running - arreglar logica
    contador = veces
    totalinstrucciones = instrucciones 
    while contador < 3: #se realizan solo 3 instrucciones por vez
        if totalinstrucciones > 0:
            print('Se estan procesando %s instrucciones del proceso %s' % (instrucciones, name))
            contador = contador + 1
            totalintrucciones = totalinstrucciones - 1
            yield env.timeout(5)
        else:
            contador = 4
            yield env.timeout(5)
        yield env.timeout(5)

def proceso(name, env, SistemaO, memoria, instrucciones, veces):
        #agregar while
        #cola de ready
    if instrucciones>0:
        with SistemaO.InstruccionesDisponibles.request() as req:
            yield req
            if instrucciones>0:
                print ""
                print('Las instrucciones que hay son: %s de %s' % (instrucciones,name))
                env.process(procesando(env, name, instrucciones, veces))
                instrucciones = instrucciones - veces
                print('Las instrucciones que quedan son %s de %s' % (instrucciones,name)) #borrar
                yield env.timeout(5)
                #waiting o ready again
                if instrucciones>0: #el waiting lo hace si aun quedan instrucciones
                    waiting = random.randint(1,2)
                    if waiting == 1:
                        yield env.timeout(7) #hacemos un delay de 7 unidades
                        print "Hice un delay de 7"
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones, veces))
                    if waiting == 2:
                        print "otra vez en cola... %s" % name
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones, veces))
                else: #Prueba de que si ya no hay instrucciones
                    print "------Ya no hay instrucciones %s" % (env.now)
                    yield SistemaO.RAM.put(memoria)
                    print('DONE procesos %s en %s ' % (name,env.now)) #terminated

def setmemoria(env, name, memoria): #se asigna memoria a proceso
    print " "
    print('El proceso %s acaba de entrar al sistema en %s' % (name, env.now))
    print ""
    print 'El nivel de memoria es %s' % SistemaO.RAM.level
    with SistemaO.RAMdisponibles.request() as req:
        if SistemaO.RAM.level <= 0: #si el sistema ya no tiene memoria, el proceso espera
            yield req
            
        print('Proceso %s tiene %s de memoria en %s' % (name,memoria,env.now))
        yield SistemaO.RAM.get(memoria) #ready con memoria asignada

def generadorProcesos(env, SistemaO, cantprocesos, intervalo, veces): #new process
    global instrucciones
    for i in range(cantprocesos):
        memoria = random.randint(1,10) #cant de memoria a usar
        instrucciones = random.randint(1,10) #cant de instrucciones a procesar
        env.process(setmemoria(env,i,memoria))
        env.process(proceso(i, env, SistemaO, memoria, instrucciones, veces))
        yield env.timeout(2)

env = simpy.Environment() #se crea ambiente
SistemaO = SistemaOperar(env) #instancia objeto de sistema operativo 
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
veces = 3 #numero de instrucciones que el procesador procesa por unidad de timpo
intervalo = 10 #intervalo al que se realizara random de memoria
cantprocesos = 4 #cantidad de procesos a realizar SO
genProcesos = env.process(generadorProcesos(env, SistemaO, cantprocesos, intervalo, veces)) #generan procesos
env.run(40)
