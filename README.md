# MonopolyArgentino
Juego de Monopoly tradicional basado en Argentina hecho en Python
Por: Jonathan Ramirez, Mateo Navarro, Brandon Moreyra  y Axel Cavero

**Introducción:**

El juego es una competencia de estrategia y gestión económica donde el objetivo es comprar todas las propiedades posibles y llevar a la bancarrota a los demás jugadores.
Se avanza con dos dados, se invierte el dinero inicial ($1000) en propiedades, servicios (Luz/Agua) y transporte. Gana el último jugador que conserve su dinero.

Reglas:

Cada jugador por turno arrojará dos dados cual suma ambos indica el avance del jugador.

Cada jugador empieza con $1500 con los cuales compra propiedades, paga impuestos al banco y/o al/los jugador/es contrario.

El ganador es el último jugador con dinero, para esto debe conseguir que el resto pierda todo el suyo. 

Las propiedades se pueden comprar o no. La clave está en saber administrar la economía personal de cada jugador decidiendo cuando y no comprar.

Cada propiedad posee un color, al poseer todas las propiedades del color que indican su precio y a la vez su valor a pagar.

Ciertas casillas benefician o empeoran la economia del jugador. Las casillas "de suerte" brindan una tarjeta aleatoria.

Por cada vuelta al tablero c/jugador cobra $200 lo cual aumenta sus posibilidades de seguir con vida.

Casilleros (40):

Cada casilero tendrá su: id, nombre, color de grupo
siempre y cuando no sean propiedades

1) Inicial (Indica inicio y la vuelta completa del tablero)
2) Florencio Varela {Marron} (Propiedad de $50)
3) Impuesto medio (Impuesto que resta $100)
4) Temperley {Marron} (Propiedad de $60)
5) Suerte (Especial) (Da una tarjeta de suerte)
6) Lineas de Colectivo (Especial) (Propiedad de transporte que vale $150)
7) Berazategui {Celeste} (Propiedad que vale $100
8) Suerte (Especial) (Da una tarjeta de suerte)
9) Quilmes{Celeste} (Propiedad que vale $110)
10) Lomas de Zamora {Celeste} (Propiedad que vale $120)
11) visita a la carcel (Especial) (Casilla libre donde también van a parar los jugadores arrestados)
12) Avellaneda {Rosa} (Propiedad que vale $140)
13) Compañia de luz (Especial) (Propiedad de luz que vale $150)
14) Lanús {Rosa} (Propiedad que vale $150)
15) La Tablada {Rosa} (Propiedad que vale $160)
16) Linea de Trenes (Especial) (Propiedad de transporte que vale $150)
17) Moreno {Naranja} (Propiedad que vale $180)
18) Suerte (Especial) (Da una tarjeta de suerte)
19) Loma Hermosa {Naranja} (Propiedad que vale $190)
20) Hurlingham {Naranja} (Propiedad que vale $200)
21) Descanso y recibo de impuestos acumulados (especial)(Casilla en la que recibes los impuestos del banco)
22) Villa Bosch {Rojo} (Propiedad que vale $220)
23) San Martin {Rojo} (Propiedad que vale $230)
24) Compañia de Agua (Especial) (Propiedad de agua que vale 150)
25) Tigre {Rojo} (Propiedad que vale $240)
26) Lienas de barcos (Especial) (Propiedad de transporte que vale $150)
27) San Isidro {Amarillo} (Propiedad que vale $260)
28) Olivos {Amarillo} (Propiedad que vale $270)
29) Suerte (Especial) (Da una tarjeta de suerte)
30) Vicente Lopez {Amarillo} (Propiedad que vale $280)
31) Carcel! (Especial) (Vas a la carcel y perdes dos turnos o si queres salir antes pagas $300) 
32) Devoto {Verde} (Propiedad que vale $300)
33) Nuñez{Verde} (Propiedad que vale $310)
34) Suerte (Especial) (Da una tarjeta de suerte)
35) Belgrano {Verde} (Propiedad que vale $320)
36) Linea de avión(Especial) (Propiedad de transporte que vale 150)
37) Suerte (Especial) (Da una tarjeta de suerte)
38) Palermo {Azul} (Propiedad que vale $350)
39) Impuesto de lujo (Impuesto que resta $200)
40) Puerto Madero {Azul} (Propiedad que vale $400)
    
Tarjetas de suerte:
1)  Subieron los impuestos -100 M
2)  Ganaste la loteria +150 B
3)  Se comprobo tu inocencia (vale para salir de la cárcel 1 vez) B // CANCELADA
4)  Se te acuso de fraude (vas a la cárcel) M
5)  Ganaste un sorteo del banco +100 B
6)  Pediste un prestamo y no lo pagaste a tiempo, te cobran intereses -150 M
7)  Es tu cumpleaños (cada jugador te da $50) B 
9)  Tus compañeros te pidieron plata (le das $20 a cada jugador) M
10) Visita al presidente (vas hasta Olivos, si pasa por la salida cobra el dinero) B
11) Tomaste el bondi equivocado retrocedes 3 casilleros M
12) Te paro la policia para ser testigo, perdes un turno M
13) Perdiste la billetera -$40 M
14) Ganaste la rifa del dia del padre ganaste $50 B
15) Dia del empleado municipal ganaste 1 turno B
16) Error bancario todos ganan $100 B
17) Cayo mercado pago todos pierden $100 M
18) Pagas impuesto a la ganancia - $100 M 
19) Argentina gana el mundial, feriado nacional, ganas un turno B
20) Te multan por exceso de velocidad -$200 M (y vas preso)
21) Recibiste una transferencia equivocada +200 B 



https://gemini.google.com/share/455ba8d9bd2f
