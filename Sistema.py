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
                print('El proceso al llegar en %s esta esperando...' % env.now) #aqui se aplica el waiting
            yield env.timeout(5)

def procesando(env, name, instrucciones): #running - arreglar logica
    contador = 0
    totalinstrucciones = instrucciones 
    while contador < 3: #se realizan solo 3 instrucciones por vez
        if instrucciones > 0:
            print('Se estan procesando instrucciones del proceso %s' % name)
            contador = contador + 1
            totalintrucciones = totalinstrucciones - 1
        else:
            contador = 4
        yield env.timeout(5)

def proceso(name, env, SistemaO, memoria, instrucciones):
        #agregar while
        #cola de ready
    if instrucciones>0:
        with SistemaO.InstruccionesDisponibles.request() as req:
            yield req
            if instrucciones>0:
                print('Las instrucciones que hay son: %s' % instrucciones)
                env.process(procesando(env, name, instrucciones))
                instrucciones = instrucciones - 3
                print('Las instrucciones que quedan son %s' % instrucciones) #deberia de aparecer la actualizada pero no se como :D
                yield env.timeout(5)
                #agregar waiting
                if instrucciones>0: #el waiting lo hace si aun quedan instrucciones
                    waiting = random.randint(1,2)
                    if waiting == 1:
                        yield env.timeout(7) #hacemos un delay de 7 unidades
                        print "Hice un delay de 7"
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones))
                    if waiting == 2:
                        env.process(proceso(name, env, SistemaO, memoria, instrucciones))
                else: #Prueba de que si ya no hay instrucciones
                    print "------Ya no hay instrucciones %s" % (env.now)
                    yield SistemaO.RAM.put(memoria)

    print('DONE procesos %s en %s ' % (name,env.now)) #terminated

def setmemoria(env, name, memoria):
    print " "
    print('El proceso %s acaba de entrar al sistema en %s' % (name, env.now))
    print ""
    print 'El nivel de memoria es %s' % SistemaO.RAM.level
    with SistemaO.RAMdisponibles.request() as req:
        if SistemaO.RAM.level <= 0:
            yield req
            
        print('Proceso %s tiene %s de memoria en %s' % (name,memoria,env.now))
        yield SistemaO.RAM.get(memoria) #ready con memoria asignada

def generadorProcesos(env, SistemaO, cantprocesos, intervalo): #new process
    global instrucciones
    for i in range(cantprocesos):
        memoria = random.randint(1,10) #cant de memoria a usar
        instrucciones = random.randint(1,10) #cant de instrucciones a procesar
        env.process(setmemoria(env,i,memoria))
        env.process(proceso(i, env, SistemaO, memoria, instrucciones))
        yield env.timeout(2)

env = simpy.Environment() #se crea ambiente
SistemaO = SistemaOperar(env) #instancia objeto de sistema operativo 
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
intervalo = 10 #intervalo al que se realizara random de memoria
cantprocesos = 5 #cantidad de procesos a realizar SO
genProcesos = env.process(generadorProcesos(env, SistemaO, cantprocesos, intervalo)) #generan procesos
env.run(40)
