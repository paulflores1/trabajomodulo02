import requests
from tabulate import tabulate
import mysql.connector


URL = "https://restcountries.com/v3.1/region/America"

response = requests.get(URL)
if response.status_code == 200:
    print("----Conexión exitosa a la API----")
    datos_paises = response.json()
    filas = []
    for pais in datos_paises:
        nombre = pais.get('name', {}).get('common', 'N/A')
        capital = pais.get('capital', ['N/A'])[0]
        poblacion = pais.get('population', 'N/A')
        region = pais.get('region', 'N/A')
        filas.append([nombre, capital, poblacion, region])

    encabezados = ["Nombre", "Capital", "Población", "Región"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))

    #CARGAMOS A LA BASE DE DATOS
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_g6"
        )
        if conexion.is_connected():
            print("----Conexión exitosa a la base de datos----")
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paises (
                    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(255),
                    capital VARCHAR(255),
                    poblacion BIGINT,
                    region VARCHAR(255)
                )
            """)
            
            #insertar datos
            for pais in filas:
                cursor.execute("""
                    INSERT INTO paises (nombre, capital, poblacion, region)
                    VALUES (%s, %s, %s, %s)
                """, pais)
            conexion.commit()
            print("----Datos insertados correctamente en la base de datos----")
            print("Mostrando datos desde la base de datos:")
            cursor.execute("SELECT * FROM paises")
            paises_db = cursor.fetchall()
            encabezados_db = ["ID", "Nombre", "Capital", "Población", "Región"]
            print(tabulate(paises_db, headers=encabezados_db, tablefmt="grid"))
            
            conexion.close()
        else:
            print("Error al conectar a la base de datos")   

    except mysql.connector.Error as err:
        print(f"Error: {err}")
else:
    print(f"Error al conectar a la API: {response.status_code}")          