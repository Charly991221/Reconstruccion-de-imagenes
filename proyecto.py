import numpy as np
import cv2
import random

def crearPoblacion(individuos):
    poblacion = []
    for i in range(individuos):
        poblacion.append(np.random.randint(0, 255, (50, 50), np.uint8))
    
    return poblacion

def fitness(poblador):

    valorFitness = 0

    for i in range(len(poblador)):
        for j in range(len(poblador)):
            if poblador[i][j] == target[i][j]:
                valorFitness += 1

    print("FITNESS ", valorFitness)
    return valorFitness

def seleccion1(poblacionCalificada, cantidadParticipantes):

    mejoresDeCompetencia = []
    seleccionados = []

    participantesOrdenados=sorted(poblacionCalificada,key=lambda p: p[1])
    mejoresDeCompetencia = participantesOrdenados[len(participantesOrdenados)-cantidadParticipantes:]

    for i in range(len(mejoresDeCompetencia)):
        seleccionados.append(mejoresDeCompetencia[i][0])

    return seleccionados

def seleccion2(poblacionCalificada, cantidadSeleccionados):

    grupos = []
    seleccionados = []
    participantesTorneo = 5

    for i in range(cantidadSeleccionados):
        for j in range(participantesTorneo):
            participante = poblacionCalificada[np.random.randint(0,len(poblacionCalificada)-1)]
            grupos.append(participante)

        participantesOrdenados=sorted(grupos,key=lambda p: p[1])
        grupos = []
        seleccionado = participantesOrdenados[len(participantesOrdenados)-1][0]

        seleccionados.append(seleccionado)

    return seleccionados

def procesarCalificacion(poblacion):
    
    listaCalificada = []
    for i in range(len(poblacion)):
        poblador = poblacion[i]
        valor = fitness(poblador)

        listaCalificada.append((poblador,valor))
    
    return listaCalificada

def reproduccion(poblacion,seleccionados):

    for i in range(len(poblacion)):

        padre1 = seleccionados[np.random.randint(0,len(seleccionados)-1)]
        padre2 = seleccionados[np.random.randint(0,len(seleccionados)-1)]

        puntoDeReproduccionX = np.random.randint(1,len(target)-1)
        puntoDeReproduccionY = np.random.randint(1,len(target)-1)

        poblacion[i][:puntoDeReproduccionX][:puntoDeReproduccionY] = padre1[:puntoDeReproduccionX][:puntoDeReproduccionY]
        poblacion[i][puntoDeReproduccionX:][puntoDeReproduccionY:] = padre2[puntoDeReproduccionX:][puntoDeReproduccionY:]

    return poblacion

def mutacion(poblacion,probabilidadMutacion):

    for i in range(len(poblacion)):
        if random.random() <= probabilidadMutacion:
            puntoMutarX = random.randint(0,len(target)-1)
            puntoMutarY = random.randint(0,len(target)-1)
            valorMutador = np.random.randint(0,255)

            while valorMutador == poblacion[i][puntoMutarX][puntoMutarY]:
                valorMutador = np.random.randint(0,255)

            poblacion[i][puntoMutarX][puntoMutarY] = valorMutador

    return poblacion

iteraciones = 50000
cantidadPobladores = 2000
cantidadParticipantes = 200
probabilidadDeMutar = 0.9
pobladores = crearPoblacion(cantidadPobladores)
target = cv2.imread("E:\Reconstruccion de imagenes\imagen.png", 0)
cv2.imshow('Imagen Original', cv2.resize(target.reshape(50,50),(200,200),interpolation = cv2.INTER_NEAREST))
cv2.waitKey(1)

for i in range(iteraciones):
    print("GENERACION ", i)

    procesarPoblacion = procesarCalificacion(pobladores)
    candidatos = seleccion1(procesarPoblacion,cantidadParticipantes)
    reproductor = reproduccion(pobladores,candidatos)
    mutados = mutacion(reproductor,probabilidadDeMutar)

    cv2.imshow('Resultado', cv2.resize(mutados[0],(200,200),interpolation = cv2.INTER_NEAREST))
    cv2.waitKey(1)