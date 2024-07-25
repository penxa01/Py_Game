import pygame
import sys
import random
import os 

def Maximo():
    global PuntuacionMaxima
    if PuntuacionActual > PuntuacionMaxima:
        PuntuacionMaxima = PuntuacionActual
    recsPuntuacion.clear()
    SonidoMuerte.play()

def VerPuntuaciones():
    if juegoActivo:
        puntuacion = txt(PuntuacionActual, BLANCO)
        puntuacionRect= puntuacion.get_rect(center = (round(Tamano_ventana[0]/2),150))
        Ventana.blit(puntuacion,puntuacionRect)
    else:
        puntuacionAc = txt( "Puntuacion:"+ str(PuntuacionActual),BLANCO)
        puntuacionAcRect = puntuacionAc.get_rect(center = (round(Tamano_ventana[0]/2),150))
        Ventana.blit(puntuacionAc,puntuacionAcRect)

        puntuacionMax = txt(" Puntuacion Maxima:" + str(PuntuacionMaxima), BLANCO)
        puntuacionMaxRect = puntuacionMax.get_rect(center = (round(Tamano_ventana[0]/2),628))
        Ventana.blit(puntuacionMax,puntuacionMaxRect)

def txt(text,color):
    texto = FuenteDeTexto.render(str(text), True, color)
    return texto

def EliminarTuberia():
    if len(tuberias)> 2:
        tuberias.pop(0)

def reset():
    global personajeRect,movimiento,PuntuacionActual
    movimiento = 0
    PuntuacionActual = 0
    personajeRect.center= (100,384)
    tuberias.clear()

def MovimientoTuberias():
    for conjuntoTuberias in tuberias:
        for tuberia in conjuntoTuberias:
            tuberia.x -= velocidadTuberias
            if tuberia.midbottom[1] > Tamano_ventana[1]:
                Ventana.blit(tuberiaNormal,tuberia)
            else:
                Ventana.blit(tuberiaInvertida,tuberia)
    
    for rect in recsPuntuacion:
        rect.x -= velocidadTuberias

def CrearTuberias():
    PosicionAleatY = random.choice(PosicionTuberiasY)
    rectTuberia = tuberiaNormal.get_rect(midtop =(PosicionTuberiasX,PosicionAleatY))
    rectInversa = tuberiaInvertida.get_rect(midbottom = (PosicionTuberiasX,PosicionAleatY - separacion))
    tuberia= [rectTuberia,rectInversa]
    rectPuntuacion = pygame.rect.Rect((rectInversa.bottomright),(10,separacion))
    recsPuntuacion.append(rectPuntuacion)
    return tuberia

def CargaryEscalar(ruta,alpha):

    rutaAbsoluta = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
    Archivo = os.path.join(rutaAbsoluta, ruta)

    if (alpha == True):
        imagen= pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.rotozoom(imagen,0,1.5).convert_alpha()
    elif ( ruta == "sprites/background-day.png"):
        imagen= pygame.image.load(ruta).convert()
        imagen = pygame.transform.rotozoom(imagen,0,1.8).convert()
    else:
        imagen= pygame.image.load(ruta).convert()
        imagen = pygame.transform.rotozoom(imagen,0,1.5).convert()
    return imagen


def rotacion(pajaro):
    nuevoSurface= pygame.transform.rotozoom(pajaro,-movimiento* VelocidadRotacion,1)
    return nuevoSurface

def Aleteo():
    global movimiento
    movimiento = 0
    movimiento -= saltar
    SonidoAleteo.play()


def comprobarColision():
    global juegoActivo , PuntuacionActual
    #Comprobacion cuando el Personaje toca el suelo
    if personajeRect.bottom >= 675:
        juegoActivo = False
    #Comprobacion cuando nuestro personaje toque la parte superior de la ventana
    if personajeRect.top <= 0:
        juegoActivo = False
    #Comprobacion de colision de tuberias
    for conjuntoTuberias in tuberias:
        for tuberia in conjuntoTuberias:
            if tuberia.colliderect(personajeRect):
                juegoActivo = False
                Maximo()
    
    for i in range(len(recsPuntuacion)-1):
        if recsPuntuacion[i].colliderect(personajeRect):
            recsPuntuacion.pop(i)
            PuntuacionActual += 1
            SonidoPunto.play()


def gravedadPersonaje():
    global movimiento
    movimiento += gravedad
    personajeRect.y += movimiento

def dibujarsuelo():
    global sueloPosX
    Ventana.blit( suelo, (sueloPosX,675))
    Ventana.blit(suelo, (sueloPosX + suelo.get_width(),675))

    sueloPosX -= 1

    if sueloPosX <= -suelo.get_width():
        sueloPosX = 0 

def dibujarfondo():
    global sueloPosXfondo
    Ventana.blit( fondo, (sueloPosXfondo,-40))
    Ventana.blit(fondo, (sueloPosXfondo + suelo.get_width(),-40))

    sueloPosXfondo -= 0.5

    if sueloPosXfondo <= -suelo.get_width():
        sueloPosXfondo = 0 



pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16 ,channels = 1, buffer = 512)
Tamano_ventana= (432, 768)

Ventana= pygame.display.set_mode((Tamano_ventana))
reloj=pygame.time.Clock()
CambiarImagen = pygame.USEREVENT
pygame.time.set_timer(CambiarImagen,250)
CREARTUBERIAS = pygame.USEREVENT + 1
pygame.time.set_timer(CREARTUBERIAS,1200)

sueloPosX= 0
sueloPosXfondo= 0
movimiento= 0
gravedad= 0.15
juegoActivo = False
saltar = 5.5
VelocidadRotacion= 3
imagenPersonaje = 0
tuberias =[]
velocidadTuberias = 3
PosicionTuberiasX =  Tamano_ventana[0] + 100
PosicionTuberiasY = (300,400,500,600)
separacion = 200
PuntuacionActual = 0
PuntuacionMaxima = 0
BLANCO =(0,0,0)
recsPuntuacion = []

fondo=CargaryEscalar("sprites/background-day.png",False)
suelo= CargaryEscalar("sprites/base.png",False)
personaje0= CargaryEscalar("sprites/yellowbird-downflap.png",True)
personaje1= CargaryEscalar("sprites/yellowbird-midflap.png",True)
personaje2= CargaryEscalar("sprites/yellowbird-upflap.png",True)
Personajes = (personaje0,personaje1,personaje2)
personajeRect= personaje1.get_rect(center = (100,384))
tuberiaNormal = CargaryEscalar("sprites/pipe-green.png",True)
tuberiaInvertida = pygame.transform.flip(tuberiaNormal,False,True)
ImagenGameOver = CargaryEscalar("sprites/message.png",True)
FuenteDeTexto = pygame.font.Font("04B_19.TTF", 30 )
RectGameOver= ImagenGameOver.get_rect(center=(round(Tamano_ventana[0]/2), round(Tamano_ventana[1]/2)))
SonidoAleteo =pygame.mixer.Sound("sounds/sfx_wing.wav")
SonidoMuerte = pygame.mixer.Sound("sounds/sfx_hit.wav")
SonidoPunto = pygame.mixer.Sound("sounds/sfx_point.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if juegoActivo:
                    Aleteo()
                else:
                    reset()
                    juegoActivo= True
        if event.type == CambiarImagen and juegoActivo:
            if imagenPersonaje >= 2:
                imagenPersonaje = 0
            else:
                imagenPersonaje+= 1
        if event.type == CREARTUBERIAS and juegoActivo:
            tuberias.append(CrearTuberias())
            EliminarTuberia()

    for rect in recsPuntuacion:
        pygame.draw.rect(Ventana,(0,0,0),rect)
    Ventana.fill((0,0,0))
    
    dibujarfondo()
    if juegoActivo:
        comprobarColision()
        MovimientoTuberias()
        Ventana.blit(rotacion(Personajes[imagenPersonaje]),personajeRect)
        gravedadPersonaje()
    else:
        Ventana.blit(ImagenGameOver,RectGameOver)
    
    VerPuntuaciones()
    dibujarsuelo()
    
    pygame.display.update()

    reloj.tick(120)