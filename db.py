"""
Pokemon Scraper Module
Author: Tau Adegun
Date: May 2025
"""

import sqlite3  # This lets us use SQLite in Python

# Name of the file where our database will be stored
DB_NAME = "pokemon.db"

def init_db():
    """
    Set up the database and make a table if it doesn't exist.
    The table will store info about Pokémon.
    """
    conn = sqlite3.connect(DB_NAME)  # Connect to the database file
    cur = conn.cursor()  # Get a cursor to do database work

    # Make a table with columns to store Pokémon info
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_info (
            name TEXT PRIMARY KEY,
            types TEXT,
            hp INTEGER,
            attack INTEGER,
            defense INTEGER,
            abilities TEXT
        )
    """)

    conn.commit()  # Save the changes
    conn.close()  # Close the connection

def get_pokemon_from_db(name):
    """
    Look up a Pokémon by name in the database.
    Returns one row with that Pokémon's info if it exists.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM pokemon_info WHERE name = ?", (name.capitalize(),))
    result = cur.fetchone()  # Get one matching row

    conn.close()
    return result

def save_pokemon_to_db(data):
    """
    Add new Pokémon info to the database.
    Takes a dictionary with name, types, hp, attack, defense, abilities.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO pokemon_info
        (name, types, hp, attack, defense, abilities)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data['name'], data['types'], data['hp'], data['attack'],
          data['defense'], data['abilities']))

    conn.commit()
    conn.close()

	
