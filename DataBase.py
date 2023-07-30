#!/usr/bin/env python3
import sqlite3
import bcrypt

# Connect to the SQLite database
connection = sqlite3.connect('players.db')
cursor = connection.cursor()

# Create the players table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        password_hash TEXT,
        balance INTEGER,
        game_state BLOB
    )
''')
connection.commit()

def reg_player(name, password, intitial_balance):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt,gensalt()).decode('utf-8')
     # Insert the player data into the database
    cursor.execute('''
        INSERT INTO players (name, password_hash, balance)
        VALUES (?, ?, ?)
    ''', (name, password_hash, initial_balance))
    connection.commit()

def verify_player(name, password):
    #Retreive store pass
    cursor.execute('''
        SELECT password_hash FROM players WHERE name = ?
''', (name,))
    row = cursor.fetchone()
    if (not row):
        return False
    #Exctract the pass hash
    stored_password_hash = row[0]
    #Check if the pass matches the sotred hash
    return bcrypt.checkpw(password.encode('utf-8'), stored_password_hashencode('utf-8'))