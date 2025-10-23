import random

def aleatorio():
    dado=random.randint(1,6)
    
    return dado

jugadores=int(input("ingrese cantidad de usuarios: "))

lista_jugadores = list(range(1, jugadores + 1))

tirada = 1
while tirada:
    for jugador in lista_jugadores:
        print(f"turno del jugador {jugador}")
        tirada=int(input("1 para tirar: "))
        
        print("el jugador 1 a tirado")
        if tirada==1:
            dado1= aleatorio()
            dado2= aleatorio()
            print(f"dado 1={dado1} y dado 2 ={dado2}")
            suma_dados= dado1 + dado2
            print(f"el jugador avanza {suma_dados}")
