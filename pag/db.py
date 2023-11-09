import serial
import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        conexion = sqlite3.connect("juego.db")
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Partida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Partida INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ) """)
        cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS ajuste_zona_horaria AFTER INSERT ON Partida
        BEGIN
        UPDATE Partida SET timestamp = DATETIME('NOW', '-3 hours')  WHERE rowid = new.rowid;
        END"""
                    )
        conexion.commit()
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        while True:
         try:
               data = ser.readline().decode().strip()
        
               nivel = int(data)
            
               # Insertar los datos en la tabla
               cursor.execute("INSERT INTO Partida (nivel) VALUES (?)", (nivel,))
               conexion.commit()
            
               print(f" el Nivel Máximo alcanzado es {nivel}")
            
         except KeyboardInterrupt:
             print("Deteniendo la recepción de datos.")
             break

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)