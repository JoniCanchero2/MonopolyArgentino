import random

# Definición de las tarjetas de Suerte (19 tarjetas personalizadas)
#
# Tipos de "accion" implementados:
# - "money": El jugador actual recibe/paga "valor".
# - "move": Mueve al jugador según "tipo_movimiento".
# - "money_per_player": El jugador actual recibe "valor" de cada otro jugador activo.
# - "pay_per_player": El jugador actual paga "valor" a cada otro jugador activo.
# - "money_all_interact": Todos los jugadores activos reciben/pagan "valor".
# - "extra_turn": El jugador actual gana un turno extra.
# - "skip_turn_message": El jugador pierde su turno de tirada de dados.

SUERTE_CARDS = [
    {
        "mensaje": "1. Subieron los impuestos. Pagas $100.",
        "accion": "money",
        "valor": -100,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "2. ¡Ganaste la lotería! Cobras $150.",
        "accion": "money",
        "valor": 150,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "3. Se te acusa de fraude. ¡Ve directo a la Cárcel! No pases por Salida.",
        "accion": "move",
        "valor": 10,  # Posición de la Cárcel
        "tipo_movimiento": "absolute_jail" 
    },
    {
        "mensaje": "4. Ganaste un sorteo del banco. Cobras $100.",
        "accion": "money",
        "valor": 100,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "5. Pediste un préstamo y no lo pagaste a tiempo. Te cobran intereses. Paga $150.",
        "accion": "money",
        "valor": -150,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "6. ¡Es tu cumpleaños! Cada jugador activo te da $50.",
        "accion": "money_per_player",
        "valor": 50,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "7. Tus compañeros te pidieron plata. Le das $20 a cada jugador activo.",
        "accion": "pay_per_player",
        "valor": 20,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "8. Visita al presidente. Avanzas hasta Olivos (Posición 39). Si pasas Salida, cobra $200.",
        "accion": "move",
        "valor": 39,  # Asumiendo Posición 39 como Olivos
        "tipo_movimiento": "absolute_pass_go" 
    },
    {
        "mensaje": "9. Tomaste el bondi equivocado. Retrocedes 3 casilleros.",
        "accion": "move",
        "valor": -3,
        "tipo_movimiento": "relative"
    },
    {
        "mensaje": "10. Te paró la policía para ser testigo. Pierdes tu turno de dados.",
        "accion": "skip_turn_message",
        "valor": 0,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "11. Perdiste la billetera. Paga $40.",
        "accion": "money",
        "valor": -40,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "12. Ganaste la rifa del dia del padre. Cobras $50.",
        "accion": "money",
        "valor": 50,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "13. Día del empleado municipal. ¡Ganas 1 turno extra!",
        "accion": "extra_turn",
        "valor": 1,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "14. Error bancario. Todos los jugadores activos ganan $100.",
        "accion": "money_all_interact",
        "valor": 100,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "15. Cayó Mercado Pago. Todos los jugadores activos pierden $100.",
        "accion": "money_all_interact",
        "valor": -100,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "16. Pagas impuesto a la ganancia. Paga $100.",
        "accion": "money",
        "valor": -100,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "17. Argentina gana el mundial, feriado nacional. ¡Ganas 1 turno extra!",
        "accion": "extra_turn",
        "valor": 1,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "18. Te multan por exceso de velocidad. Paga $200.",
        "accion": "money",
        "valor": -200,
        "tipo_movimiento": "none"
    },
    {
        "mensaje": "19. Recibiste una transferencia equivocada. Cobras $200.",
        "accion": "money",
        "valor": 200,
        "tipo_movimiento": "none"
    },
]

def get_shuffled_suerte_deck():
    """Retorna una copia mezclada del mazo de cartas de Suerte."""
    deck = list(SUERTE_CARDS)
    random.shuffle(deck)
    return deck