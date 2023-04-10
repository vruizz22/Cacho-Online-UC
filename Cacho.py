import random
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from Cacho import CachoGame

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Ruta principal para mostrar la página del juego
@app.route("/")
def index():
    return render_template("cacho.html")

# Función que se ejecuta cuando se conecta un nuevo cliente al servidor de websockets
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

# Función que se ejecuta cuando se desconecta un cliente del servidor de websockets
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

# Ruta para procesar la solicitud de lanzamiento de dados y devolver los resultados
@app.route("/lanzar_dados", methods=["POST"])
def lanzar_dados():
    dados = []
    for i in range(5):
        dados.append(random.randint(1,6))
    # Envía los resultados a todos los clientes conectados a través del canal "resultados"
    socketio.emit('resultados', dados)
    return jsonify(dados)

# Ruta para procesar las apuestas y verificar si son correctas o no
@app.route("/verificar_apuesta", methods=["POST"])
def verificar_apuesta():
    datos = request.get_json()
    pinta = datos["pinta"]
    cantidad = datos["cantidad"]
    dados = datos["dados"]
    dados_filtrados = [dado for dado in dados if dado == pinta or dado == 1]
    if len(dados_filtrados) >= cantidad:
        resultado = {"resultado": "correcto"}
    else:
        resultado = {"resultado": "incorrecto"}
    # Envía el resultado de la apuesta al cliente que la realizó a través del canal "resultado_apuesta"
    socketio.emit('resultado_apuesta', resultado)
    return jsonify(resultado)

if __name__ == "__main__":
    socketio.run(app)




class CachoGame:

    def __init__(self, players):

        self.players = players

        self.current_player = 0

        self.current_bet = None

        self.dice = [0] * 5

        self.pintas = ['Ases', 'Reyes', 'Caballos', 'Sotas', 'Seises']

    

    def play(self):

        print("Comenzando el juego de cacho...")

        print(f"Jugadores: {self.players}")

        while True:

            self.roll_dice()

            print(f"\nJugador actual: {self.players[self.current_player]}")

            print(f"Dados en la mesa: {self.dice}")

            print(f"Apuesta actual: {self.current_bet}")

            bet = self.make_bet()

            if bet is None:

                break

            if bet == "calzo":

                if self.check_calzo():

                    self.players[self.current_player] += 1

                    print(f"{self.players[self.current_player]} ha ganado un dado!")

                else:

                    print("La apuesta era incorrecta, se pierde un dado!")

                    self.players[self.current_player] -= 1

                    if self.players[self.current_player] == 0:

                        break

            else:

                self.current_bet = bet

    

    def roll_dice(self):

        print("Tirando los dados...")

        self.dice = [random.randint(1,6) for _ in range(5)]

    

    def make_bet(self):

        if self.current_bet is None:

            bet_str = input("Haz tu primera apuesta (cantidad pinta): ")

        else:

            bet_str = input("Haz tu siguiente apuesta (cantidad pinta/dudo/calzo): ")

        if bet_str.lower() == "dudo":

            if self.check_bet():

                print("La apuesta era correcta, el otro jugador pierde un dado!")

                self.players[(self.current_player + 1) % len(self.players)] -= 1

                if self.players[(self.current_player + 1) % len(self.players)] == 0:

                    return None

            else:

                print("La apuesta era incorrecta, tú pierdes un dado!")

                self.players[self.current_player] -= 1

                if self.players[self.current_player] == 0:

                    return None

            return self.current_bet

        elif bet_str.lower() == "calzo":

            return bet_str

        else:

            cantidad, pinta = bet_str.split()

            cantidad = int(cantidad)

            if cantidad > sum(self.dice):

                print("La apuesta es incorrecta porque la cantidad es mayor que el número total de dados en la mesa!")

                return self.make_bet()

            if self.current_bet is None or cantidad >= self.current_bet[0]:

                if pinta not in self.pintas:

                    print("La apuesta es incorrecta porque la pinta no es válida!")

                    return self.make_bet()

                if self.current_bet is None or self.pintas.index(pinta) >= self.pintas.index(self.current_bet[1]):

                    return (cantidad, pinta)

                else:

                    print("La apuesta es incorrecta porque la pinta es inferior a la pinta actual!")

                    return self.make_bet()

            else:

                print("La apuesta es incorrecta porque la cantidad es inferior a la cantidad actual!")

                return self.make_bet()

    def obtener_pinta():
        pintas = ["Ases", "Reyes", "Caballos", "Sotas", "Seises"]
        return pintas[randint(0, 4)]



# Función para obtener la cantidad de una pinta en una lista de dados

def obtener_cantidad(pinta, dados):

    cantidad = 0

    for dado in dados:

        if dado == pinta:

            cantidad += 1

    return cantidad



# Función para verificar si una apuesta es válida o no

def verificar_apuesta(apuesta, dados):

    cantidad_apuesta, pinta_apuesta = apuesta.split()

    cantidad_apuesta = int(cantidad_apuesta)

    if pinta_apuesta not in ["Ases", "Reyes", "Caballos", "Sotas", "Seises"]:

        return False

    if cantidad_apuesta > len(dados):

        return False

    if pinta_apuesta == "Ases":

        return True

    if pinta_apuesta == "Reyes":

        if obtener_cantidad("Ases", dados) >= cantidad_apuesta:

            return True

        else:

            return False

    if pinta_apuesta == "Caballos":

        if obtener_cantidad("Ases", dados) + obtener_cantidad("Reyes", dados) >= cantidad_apuesta:

            return True

        else:

            return False

    if pinta_apuesta == "Sotas":

        if obtener_cantidad("Ases", dados) + obtener_cantidad("Reyes", dados) + obtener_cantidad("Caballos", dados) >= cantidad_apuesta:

            return True

        else:

            return False

    if pinta_apuesta == "Seises":

        if obtener_cantidad("Ases", dados) + obtener_cantidad("Reyes", dados) + obtener_cantidad("Caballos", dados) + obtener_cantidad("Sotas", dados) >= cantidad_apuesta:

            return True

        else:

            return False



# Función para jugar una ronda de cacho

def jugar_ronda(jugadores, indice_jugador):

    # El jugador actual tira los dados y los oculta

    dados = []

    for i in range(5):
        dados.append(obtener_pinta())

    print(f"Jugador {indice_jugador + 1} ha tirado los dados y los ha ocultado.")

    print("")



    # Se hace la apuesta inicial

    apuesta_actual = ""

    while not verificar_apuesta(apuesta_actual, dados):

        apuesta_actual = input(f"Jugador {indice_jugador + 1}, haz tu apuesta: ")

        if not verificar_apuesta(apuesta_actual, dados):

            print("Apuesta no válida. Por favor, inténtalo de nuevo.")

            print("")

    print(f"Jugador {indice_jugador + 1} ha hecho la siguiente apuesta: {apuesta_actual}")

    print("")



    # Se inicia el turno de los demás jugadores

    jugando = True

    siguiente_jugador = (indice_jugador + 1) % len(jugadores)

    while jugando:

        respuesta = input(f"Jugador {siguiente_jugador + 1}, ¿quieres aceptar la apuesta? (s/n) ")

        if respuesta == "s":

            # El siguiente jugador acepta la apuesta y hace su propia apuesta

            apuesta_anterior = apuesta_actual

# Función para verificar si la apuesta es correcta

def verificar_apuesta(apuesta, mesa):

    cantidad_apuesta, pinta_apuesta = apuesta.split(" ")

    cantidad_apuesta = int(cantidad_apuesta)

    if pinta_apuesta == "Ases":

        pinta_apuesta_valor = 5

    elif pinta_apuesta == "Reyes":

        pinta_apuesta_valor = 4

    elif pinta_apuesta == "Caballos":

        pinta_apuesta_valor = 3

    elif pinta_apuesta == "Sotas":

        pinta_apuesta_valor = 2

    else:

        pinta_apuesta_valor = 1

    cantidad_mesa = 0

    pinta_mesa_valor = 0

    for dado in mesa:

        if dado == pinta_apuesta_valor or dado == 5:

            cantidad_mesa += 1

        if dado > pinta_mesa_valor and dado != 5:

            pinta_mesa_valor = dado

    if cantidad_apuesta > cantidad_mesa:

        return False

    elif cantidad_apuesta == cantidad_mesa and pinta_apuesta_valor <= pinta_mesa_valor:

        return False

    else:

        return True



# Función principal del juego

def jugar_cacho():

    jugadores = ["Jugador 1", "Jugador 2", "Jugador 3", "Jugador 4"]

    dados_jugadores = {jugador: 5 for jugador in jugadores}

    mesa = []

    turno = 1

    while len(jugadores) > 1:

        print("Jugadores:", jugadores)

        print("Dados de cada jugador:", dados_jugadores)

        print("Mesa:", mesa)

        jugador_actual = jugadores[0]

        print("Es el turno de", jugador_actual)

        input("Presiona enter para tirar los dados")

        dados = []

        for i in range(dados_jugadores[jugador_actual]):

            dado = random.randint(1, 6)

            dados.append(dado)

        print("Los dados son:", dados)

        mesa += dados

        apuesta_valida = False

        while not apuesta_valida:

            apuesta = input("Haz una apuesta en el formato 'cantidad pinta' (por ejemplo, '3 Reyes'): ")

            apuesta_valida = verificar_apuesta(apuesta, mesa)

            if not apuesta_valida:

                print("Apuesta no válida. Inténtalo de nuevo.")

        dudo = False

        jugadores_dudosos = []

        while not dudo:

            siguiente_jugador = jugadores[(turno % len(jugadores))]

            if siguiente_jugador not in jugadores_dudosos and siguiente_jugador != jugador_actual:

                print(siguiente_jugador, "es el siguiente jugador")

                nueva_apuesta = input("Haz una nueva apuesta o di 'dudo': ")

                if nueva_apuesta == "dudo":

                    dudo = True

                    if verificar_apuesta(apuesta, mesa):

                        print(jugador_actual, "pierde un dado")

                        dados_jugadores[jugador_actual] -= 1

                        if dados_jugadores[jugador_actual] == 0:

                            jugadores.remove(jugador_actual)

                            print(jugador_actual, "ha perdido el juego")

                            break

                    else:

                        print(siguiente_jugador, "pierde un dado")

def es_apuesta_valida(apuesta, apuesta_anterior, dados_en_mesa):

    cantidad, pinta = apuesta

    

    # Comprobamos si la cantidad es mayor o igual a la apuesta anterior

    if apuesta_anterior is not None and cantidad < apuesta_anterior[0]:

        return False

    

    # Comprobamos si la pinta es válida

    if pinta not in PINTAS:

        return False

    

    # Si la apuesta anterior es None, cualquier apuesta es válida

    if apuesta_anterior is None:

        return True

    

    cantidad_anterior, pinta_anterior = apuesta_anterior

    

    # Si la pinta de la apuesta es más alta que la pinta más alta en la mesa, es válida

    if PINTAS.index(pinta) > PINTAS.index(dados_en_mesa.obtener_pinta_mas_alta()):

        return True

    

    # Si la cantidad de la apuesta es mayor o igual a la cantidad total de dados en la mesa, es inválida

    if cantidad >= len(dados_en_mesa.dados):

        return False

    

    # Si la cantidad y la pinta son iguales a la apuesta anterior, es inválida

    if cantidad == cantidad_anterior and pinta == pinta_anterior:

        return False

    

    return True

def juego_cacho():

    # Creamos los dados y los mezclamos

    dados = [random.randint(1, 6) for _ in range(5)]

    random.shuffle(dados)

    

    # Creamos el objeto Mesa

    mesa = Mesa(dados)

    

    # Creamos una lista de jugadores y mezclamos el orden

    jugadores = ["Jugador 1", "Jugador 2", "Jugador 3", "Jugador 4"]

    random.shuffle(jugadores)

    

    # Definimos la primera apuesta y el jugador que la hace

    apuesta_actual = None

    jugador_actual = jugadores[0]

    

    # Empezamos el juego

    while len(jugadores) > 1:

        # Mostramos los dados en la mesa

        print("Dados en la mesa: ", mesa.dados)

        

        # Pedimos una apuesta al jugador actual

        apuesta = input(f"{jugador_actual}, ¿cuál es tu apuesta? ")

        cantidad, pinta = apuesta.split()

        cantidad = int(cantidad)

        

        # Comprobamos si la apuesta es válida

        if not es_apuesta_valida((cantidad, pinta), apuesta_actual, mesa):

            print("Apuesta inválida.")

            continue

# Declarar la función principal del juego

def cacho():

    # Imprimir las reglas del juego

    print("Bienvenido al juego de cacho.\nEl objetivo es adivinar y/o apostar la cantidad y la pinta de los dados que hay en la mesa.")

    print("Reglas:")

    print("- El juego se juega con cinco dados de seis caras.")

    print("- El primer jugador tira los cinco dados y oculta el resultado con su mano.")

    print("- A continuación, el jugador anuncia una pinta y una cantidad, por ejemplo 'tres seises'.")

    print("- El siguiente jugador puede aceptar la apuesta o hacer una nueva apuesta de una cantidad y una pinta diferente, pero la cantidad debe ser mayor o igual a la apuesta anterior.")

    print("- Si un jugador no cree en la apuesta del jugador anterior, puede decir 'dudo'. Entonces, se revelan los dados y se verifica si la apuesta es correcta o no.")

    print("- Si la apuesta es correcta, el jugador que dudó pierde un dado. Si la apuesta es incorrecta, el jugador que hizo la apuesta pierde un dado.")

    print("- El juego continúa con los jugadores restantes, repitiendo los pasos 3 a 6.")

    print("- El jugador que pierde todos los dados pierde el juego.")

    print("- Si un jugador logra adivinar correctamente la cantidad y la pinta de los dados totales en la mesa diciendo 'calzo', gana automáticamente un dado en el juego.")

    print("- Las pintas tienen un valor jerárquico. La jerarquía de las pintas, de mayor a menor valor, es la siguiente: Ases, Reyes, Caballos, Sotas, Seises.")

    print("- Si un jugador hace una apuesta con una pinta más alta que la pinta más alta en la mesa, esa apuesta es automáticamente correcta.")

    print("- Si un jugador hace una apuesta con una cantidad mayor que la cantidad total de dados en la mesa, esa apuesta es automáticamente incorrecta.")



    # Pedir el número de jugadores y sus nombres

    num_jugadores = int(input("¿Cuántos jugadores van a jugar?: "))

    jugadores = []

    for i in range(num_jugadores):

        nombre = input("Nombre del jugador " + str(i+1) + ": ")

        jugadores.append({"nombre": nombre, "dados": 5})



    # Establecer la ronda inicial

    ronda = 1



    # Bucle principal del juego

    while len(jugadores) > 1:

        # Imprimir la información de la ronda

        print("\nRonda " + str(ronda) + ":")

        print("Jugadores:")

        for jugador in jugadores:

            print(jugador["nombre"] + ": " + str(jugador["dados"]) + " dados")



        # Crear los dados y tirarlos

        dados = [random.randint(1, 6) for i in range(5)]

        print("Dados: " + str(dados))



        # Establecer la apuesta inicial

        jugador_actual = 0

        apuesta = {"cantidad": 0, "pinta": ""}

        while True:

            # Pedir la apuesta del jugador

            print(jugadores[jugador_actual]["nombre"] + ", es tu turno.")

            cantidad = int(input("Cantidad: "))

            pinta = input("Pinta: ")





def calzo(dados_en_mesa, apuesta):

    if apuesta == dados_en_mesa:

        print("¡Calzo! Adivinaste correctamente la cantidad y la pinta de los dados en la mesa.")

        return True

    else:

        print("Lo siento, no adivinaste correctamente la cantidad y la pinta de los dados en la mesa.")

        return False



def jugar_cacho(num_jugadores):

    # Definir los jugadores

    jugadores = []

    for i in range(num_jugadores):

        nombre = input(f"Ingrese el nombre del jugador {i+1}: ")

        jugadores.append(nombre)



    # Definir la jerarquía de las pintas

    jerarquia_pintas = ["Ases", "Reyes", "Caballos", "Sotas", "Seises"]



    # Definir el número de dados y caras

    num_dados = 5

    num_caras = 6



    # Inicializar los dados

    dados = []

    for i in range(num_dados):

        dados.append(random.randint(1,num_caras))



    # Definir el jugador inicial y la apuesta inicial

    jugador_actual = 0

    apuesta_actual = [1, "Ases"]



    # Inicializar el juego

    while True:

        print(f"Jugador actual: {jugadores[jugador_actual]}")

        print(f"Apuesta actual: {apuesta_actual[0]} {apuesta_actual[1]}")

        respuesta = input("¿Aceptas la apuesta? (S/N) ").upper()

        if respuesta == "S":

            # Si la apuesta es aceptada, el jugador lanza los dados

            dados_en_mesa = tirar_dados(num_dados, num_caras, dados)

            print(f"Dados en la mesa: {dados_en_mesa}")

            if calzo(dados_en_mesa, apuesta_actual):

                # Si el jugador adivina correctamente, gana un dado y se reinicia el juego

                print(f"{jugadores[jugador_actual]} ganó un dado.")

                dados.append(1)

                break

            else:

                # Si el jugador no adivina, pierde un dado y el siguiente jugador toma el relevo

                print(f"{jugadores[jugador_actual]} perdió un dado.")

                dados.remove(1)

                jugador_actual = (jugador_actual + 1) % num_jugadores

                apuesta_actual = [1, "Ases"]

        else:

            # Si la apuesta es rechazada, el siguiente jugador hace una nueva apuesta

            apuesta_nueva = hacer_apuesta(apuesta_actual, jerarquia_pintas)

