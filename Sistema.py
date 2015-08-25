import simpy

import random

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def proceso(env, name, procesador, driving_time, charge_duration): #agregar el parametro de ram, e instrucciones
    global totalGasStation
    # Simulate driving to the BCS
    yield env.timeout(driving_time) #El drivingTime es lo que el carro se tarda en ir de su casa a la gasolinera por asi decirlo
    llegada = env.now #llega a la estacion de servicio

    #Este arriving at quiere decir que salio en el tiempo at: numero...
    # Request one of its charging spots
    print('%s creado en el tiempo %d' % (name, env.now))
    with procesador.request() as req:  #pedimos conectarnos al cargador de bateria - cola
        yield req

        # Charge the battery
        print('%s ejecutandose en el tiempo %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s terminando de ejecutarse en el tiempo %s' % (name, env.now))
        # se hizo release automatico del cargador bcs

    tiempoTotal = env.now - llegada
    totalGasStation = totalGasStation + tiempoTotal #guardar en una lista 
    print ('%s Se tardo en cargar %s' % (name, tiempoTotal))
#
env = simpy.Environment()  #crear ambiente de simulacion
procesador = simpy.Resource(env, capacity=1) #el cargador de bateria soporta 2 carros
                                      #a la vez



totalGasStation = 0.0
nprocesos = 5
RANDOM_SEED = 42 #semilla para generar la misma serie de random
random.seed(RANDOM_SEED)
interval = 10

# crear los procesos
for i in range(nprocesos):
    t = random.expovariate(1.0 / interval)
    #poner aqui el random para la ram que consumira y se manda como parametro en carro
    #Tambien cantidad de instrucciones (entre 0 y 10)
    env.process(proceso(env, 'Proceso %d' % i, procesador, t, 5))

# correr la simulacion
env.run()

promedioGasStation = totalGasStation / nprocesos
print "El promedio fue: ", promedioGasStation
