# MonopolyArgentino
Juego de Monopoly tradicional basado en Argentina hecho en Python
Por: Jonathan Ramirez, Mateo Navarro, Brandon Moreira  y Axel Cavero\n
**Introducción:**

El juego es una competencia de estrategia y gestión económica donde el objetivo es comprar todas las propiedades posibles y llevar a la bancarrota a los demás jugadores.
Se avanza con dos dados, se invierte el dinero inicial ($1500) en propiedades, servicios (Luz/Agua) y transporte. La clave para ganar es adquirir grupos de color para poder construir casas y cobrar rentas más altas. El riesgo reside en las tiradas: sacar dados dobles tres veces seguidas resulta en arresto. Gana el último jugador que conserve su dinero.

Reglas:

Cada jugador por turno arrojará dos dados cual suma ambos indica el avance del jugador.

Si la tirada del jugador da como resultado dos dados iguales, el jugador vuelve a tirar. 
Esto se puede repetir una vez más con limite de 2 repeticiones, en caso de volver a tirar dados dobles el jugador es arrestado.

Cada jugador empieza con $1500 con los cuales compra propiedades, paga impuestos al banco y/o al/los jugador/es contrario.

El ganador es el último jugador con dinero, para esto debe conseguir que el resto pierda todo el suyo. 

Las propiedades se pueden comprar/subastar/negociar entre jugadores ya sea por otras propiedades o por dinero.

Cada propiedad posee un color, al poseer todas las propiedades del color compradas el jugador puede construir casas y cobrar más caro a los jugadores que pasen por sus propiedades.

Ciertas casillas benefician o empeoran la economia del jugador. Las casillas "de suerte" brindan una tarjeta aleatoria.

Por cada vuelta al tablero c/jugador cobra $200.

Existen varias casillas de transporte que se pueden comprar, dependiendo de esto, el jugador contrario que caiga sobre una de estas deberá pagar el valor correspondiente duplicado por cada propiedad adquirida.

Las casillas de Luz y Agua tambien son comprables, el monto a pagar del jugador que pase sobre ellas y no las tenga compradas cambiara en funcion del numero de los dados. Si el dueño de las propiedades posee solamente una, el jugador que caiga deberá pagar el cuadruple de la suma de su tirada. En caso de que el dueño posea las dos propiedades, pagará diez veces la suma de su tirada.

Casilleros (40):

cada casilero tendrá su: id, nombre, color de grupo
siempre y cuando no sean propiedades

1) Inicial (Indica inicio y la vuelta completa del tablero)
2) Florencio Varela {Marron} (Propiedad de $50)
3) Impuesto medio (Impuesto que resta $100)
4) Temperley {Marron} (Propiedad de $60)
5) Suerte (Especial) (Da una tarjeta de suerte)
6) Lineas de Colectivo (Especial) (Propiedad de transporte que vale $150)
7) Berazategui {Celeste} (Propiedad que vale $100)
8) Quilmes{Celeste} (Propiedad que vale $110)
9) Suerte (Especial) (Da una tarjeta de suerte)
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
1) pasaste por una villa y te desvalijaron -100
2) heredaste una propiedad de un abuelo en italia +150
3) te hiciste amigo de un juez (vale para salir de la cárcel 1 vez)
4) plantaron merluza en tu auto (vas a la cárcel)
5) el banco te paga +100
6) el banco te retiene plata -150
7) feliz cumpleaños! (cada jugador te da 50)
8) tus compañeros te salvan...(le das 20 a cada jugador)
9) visita al presidente (vas hasta Olivos, si pasa por la salida cobra el dinero)
10) retrocedé 3 casilleros por pete

