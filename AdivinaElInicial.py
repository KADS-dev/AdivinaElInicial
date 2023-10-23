import sqlite3
# Definición de algunos Pokémon con sus características
iniciales = [
    {"nombre": "Bulbasur", "tipo": "Planta", "Generacion": "1"},
    {"nombre": "Charmander", "tipo": "Fuego", "Generacion": "1"},
    {"nombre": "Squirtle", "tipo": "Agua", "Generacion": "1"},
    
    {"nombre": "Chikorita", "tipo": "Planta", "Generacion": "2"},
    {"nombre": "Cyndaquil", "tipo": "Fuego", "Generacion": "2"},
    {"nombre": "Totodile", "tipo": "Agua", "Generacion": "2"},
    
    {"nombre": "Treecko", "tipo": "Planta", "Generacion": "3"},
    {"nombre": "Torchic", "tipo": "Fuego", "Generacion": "3"},
    {"nombre": "Mudkip", "tipo": "Agua", "Generacion": "3"},
    
    {"nombre": "Turtwig", "tipo": "Planta", "Generacion": "4"},
    {"nombre": "Chimchar", "tipo": "Fuego", "Generacion": "4"},
    {"nombre": "Piplup", "tipo": "Agua", "Generacion": "4"},
    
    {"nombre": "Snivy", "tipo": "Planta", "Generacion": "5"},
    {"nombre": "Tepig", "tipo": "Fuego", "Generacion": "5"},
    {"nombre": "Oshawott", "tipo": "Agua", "Generacion": "5"},
    
    {"nombre": "Chespin", "tipo": "Planta", "Generacion": "6"},
    {"nombre": "Fennekin", "tipo": "Fuego", "Generacion": "6"},
    {"nombre": "Froakie", "tipo": "Agua", "Generacion": "6"},
    
    {"nombre": "Rowlet", "tipo": "Planta", "Generacion": "7"},
    {"nombre": "Litten", "tipo": "Fuego", "Generacion": "7"},
    {"nombre": "Popplio", "tipo": "Agua", "Generacion": "7"},
    
    {"nombre": "Grookey", "tipo": "Planta", "Generacion": "8"},
    {"nombre": "Scorbunny", "tipo": "Fuego", "Generacion": "8"},
    {"nombre": "Sobble", "tipo": "Agua", "Generacion": "8"},
    
    {"nombre": "Sprigatito", "tipo": "Planta", "Generacion": "9"},
    {"nombre": "Fuecoco", "tipo": "Fuego", "Generacion": "9"},
    {"nombre": "Quaxly", "tipo": "Agua", "Generacion": "9"}
    
    # Agrega más Pokémon con sus características
]


continuar = "s"

limiteGeneracional = 9

# Función para determinar el Pokémon correcto utilizando encadenamiento hacia adelante
def adivina_el_pokemon():
    
    #Pregunta sobre el tipo
    while True:
        print("¿El inicial es de tipo Fuego? s/n")
        respuesta = input()
        if respuesta == "s":
            tipo = "Fuego"
            break
        elif respuesta != "n":
            print("Escribe solo <<s>> o <<n>>")
        
        print("¿El inicial es de tipo Agua? s/n")
        respuesta = input()
        if respuesta == "s":
            tipo = "Agua"
            break
        elif respuesta != "n":
            print("Escribe solo <<s>> o <<n>>")
        
        
        print("¿El inicial es de tipo Planta? s/n")
        respuesta= input()
        if respuesta == "s":
            tipo = "Planta"
            break
        elif respuesta != "n":
            print("Escribe solo <<s>> o <<n>>")
        
        print("Intentemos de nuevo")
    #Pregunta sobre la generación:
    while True:
        print("¿El inicial de qué generación es? ¿1,2,3,4,5...?")
        generacion = int(input())
        if (generacion > 0 and generacion <=limiteGeneracional):
            break
        print("No existe esa generacion en la base de datos")
    
    #llama a la funcion para encontrar a el pokemon 
    nombre_pokemon = obtener_nombre_pokemon(tipo, generacion)
    print("El pokemon es: ", nombre_pokemon)
        
def obtener_nombre_pokemon(tipo, generacion):
    for pokemon in iniciales:
        
        if pokemon["tipo"] == str(tipo) and pokemon["Generacion"] == str(generacion):
            return pokemon["nombre"]
    #Si no encuentra coincidencia
    return None  

# Función para cargar los Pokémon desde la base de datos (si existe)
def cargar_pokemon_desde_db(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pokemons")
        pokemon_data = cursor.fetchall()
        conn.close()
        
        if pokemon_data:
            iniciales = []
            for data in pokemon_data:
                pokemon = {"nombre": data[1], "tipo": data[2], "Generacion": data[3]}
                iniciales.append(pokemon)
            return iniciales
    except sqlite3.Error:
        pass

    return None
        

# Función para guardar la lista de Pokémon en una base de datos SQLite
def guardar_pokemon_en_db(pokemon_list, db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Crea una tabla llamada 'pokemons' para almacenar los datos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemons (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            tipo TEXT,
            Generacion TEXT
        )
    ''')

    # Inserta los datos de la lista en la tabla
    for pokemon in pokemon_list:
        cursor.execute('INSERT INTO pokemons (nombre, tipo, Generacion) VALUES (?, ?, ?)',
                       (pokemon["nombre"], pokemon["tipo"], pokemon["Generacion"]))

    # Guarda los cambios en la base de datos
    conn.commit()

    # Cierra la conexión a la base de datos
    conn.close()

# Función para obtener el número de generación más alto
def obtener_generacion_mas_alta(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(Generacion AS INTEGER)) FROM pokemons")
        max_generacion = cursor.fetchone()[0]
        conn.close()
        return max_generacion
    except sqlite3.Error:
        pass

    return limiteGeneracional


# Iniciar el juego
while continuar == "s":
    # Llama a la función para guardar los Pokémon en la base de datos
    guardar_pokemon_en_db(iniciales, 'pokemones.db')
    
    iniciales = cargar_pokemon_desde_db('pokemones.db')
    limiteGeneracional = obtener_generacion_mas_alta('pokemones.db')
    print("¡Bienvenido a Adivina el Inicial!")
    print("Responde las siguientes preguntas para adivinar el Pokémon.")    
    adivina_el_pokemon()
    print("Si desea continuar presione <<s>>")
    continuar = input()
    print("¿Desea Agregar una generacion de iniciales a la base de datos? s/n")
    if ("s" == input()):
        
        print("Ingresa el nombre del inicial tipo planta: ")
        nuevoInicialPlanta = input()
        
        print("Ingresa el nombre del inicial tipo fuego: ")
        nuevoInicialFuego = input()
        
        print("Ingresa el nombre del inicial tipo agua: ")
        nuevoInicialAgua = input()
        
        limiteGeneracional += 1        
        nuevo_pokemonPlanta = {"nombre": str(nuevoInicialPlanta), "tipo": "Planta", "Generacion": str(limiteGeneracional)}
        nuevo_pokemonFuego = {"nombre": str(nuevoInicialFuego), "tipo": "Fuego", "Generacion": str(limiteGeneracional)}
        nuevo_pokemonAgua = {"nombre": str(nuevoInicialAgua), "tipo": "Agua", "Generacion": str(limiteGeneracional)}

        iniciales.append(nuevo_pokemonPlanta)
        iniciales.append(nuevo_pokemonFuego)
        iniciales.append(nuevo_pokemonAgua)
        
       