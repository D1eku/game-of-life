import pygame 
import numpy as np
import time
import sys

pygame.init()

#Ancho y alto de la pantalla
width, height = 1000,1000
#creacion de la pantalla
screen = pygame.display.set_mode((height,width));

#Color del fondo 
bg = (25,25,25)

#pintamos el fondo con el color del fondo
screen.fill(bg);

#Tamaño de las celdas
nxC, nyC = 50,50
dimCW = width/nxC
dimCH = height/nyC

#estado de las celdas. Vivas = 1, Muertas = 0
gameState = np.zeros((nxC,nyC))

# Automatas
gameState[5,3] = 1
gameState[5,3] = 1
gameState[5,3] = 1

#Automata Movil
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1

#Control de pausa
pauseExect = False


#bluce de ejecucion
while True:

	#Copia el estado inicial
	newGameState = np.copy(gameState)
	#Vuelve a pintar el mapa
	screen.fill(bg)
	#Pausa por 0.1 segundos
	time.sleep(0.1)
	#Interrupciones de teclado y raton.
	
	ev = pygame.event.get()
	#Para cada evento de ev
	for event in ev:
		#Si se detecta algun evento en el teclado
		if event.type == pygame.KEYDOWN:
			pauseExect = not pauseExect
		#Si se presiona el raton, captura el click
		mouseClick = pygame.mouse.get_pressed()
		#Si se hizo click
		if sum(mouseClick) > 0:
			posX, posY = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
			newGameState[celX, celY] = not mouseClick[2]
	#Para cada celda en eje X
	for y in range(0,nxC):
		#Para cada celda en eje Y
		for x in range(0,nyC):
			if not pauseExect:
				#Calculo del numero de los vecinos cercanos.
				n_neigh = gameState[(x-1) % nxC , (y-1)  % nyC ] + \
						  gameState[(x)   % nxC , (y - 1)% nyC ] + \
						  gameState[(x+1) % nxC ,(y-1)   % nyC ] + \
						  gameState[(x-1) % nxC ,(y)     % nyC ] + \
						  gameState[(x+1) % nxC ,(y)     % nyC ] + \
						  gameState[(x-1) % nxC ,(y+1)   % nyC ] + \
						  gameState[(x)   % nxC ,(y+1)   % nyC ] + \
						  gameState[(x+1) % nxC ,(y+1)   % nyC ] 
						  
				#Regla 1 : Una celula muerta con exactamente 3 vecinas vivas, "Revive".
				if gameState[x,y] == 0 and n_neigh == 3:
					newGameState[x,y] = 1
				#Regla 2 :Una celula viva con menos de 2 o mas de 3 vecinas vivas, "Muere"
				elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
					newGameState[x,y] = 0
					
					
			#Se crea el poligono de dibujado de celdas.
			poly = [((x)   * dimCW  , y    * dimCH),
					((x+1) * dimCW  , y    * dimCH),
					((x+1) * dimCW  ,(y+1) * dimCH),
					((x)   * dimCW  ,(y+1) * dimCH)]
						
			#Dibujamos la celda para cada par (x,y)
			if newGameState[x,y] == 0:
				pygame.draw.polygon(screen, (128,128,128),poly, 1)
			else:
				pygame.draw.polygon(screen, (255,255,255),poly, 0)
		
		#Actualizamos el estado del juego
		gameState = np.copy(newGameState)
		
	#Actualizamos la pantalla
	pygame.display.flip()
			