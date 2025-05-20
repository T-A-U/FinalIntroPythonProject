"""
Pokemon Scraper Module
Author: Tau Adegun
Date: May 2025

This module defines a function to scrape basic Pokémon data
(HP, Attack, Defense, Type, and Abilities) from https://pokemondb.net.
"""

import requests  # To make HTTP requests to the website-Requests
from bs4 import BeautifulSoup  # To go through the html content # To parse and navigate HTML content-Beautiful soup
import re  # To extract numbers using regular expressions -Regular expressions.
#These imports are what are used to scrape from the website

def scrape_pokemon_data(name):
    """
    Scrape Pokémon info from pokemondb.net.

    Given the name of a Pokémon, this function looks over the
    webpage and extracts its type(s), HP, Attack, Defense, and Abilities.

    Parameters:
        name - in string format: The name of the Pokémon the user looks up.

    Returns:
        dict: A dictionary with keys 'name', 'types', 'hp', 'attack', 'defense', 'abilities'.
              Returns None if the webpage cannot be accessed or if te data can't be parsed.

       Basically given the pokemon the user searches for it gives the name and various attributes like Hp, attack, etc, the name of the pokemon you search is given in string format else it gives none if it cant find the pokemon searched or cant parse the data.
    """
    # This the URL for the Pokémon's page - the latter part is taking the name of the pokemon the user inseerted and making it lowercase
    url = f"https://pokemondb.net/pokedex/{name.lower()}"

    # Try to download the page
    try:
        page = requests.get(url)
        page.raise_for_status()  # Show an error if the page doesn't load
    except:
        return None  # Return None if there's some network or HTTP error

    # Parse the downloaded HTML page using Beautiful Soup
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        # --- Get Pokémon Types ---
        # The below is all based on the HTML of the pokemon website page - I looked at the HTML by using the inspect tool and the web scraper downloaded from above
        # Find all <a> tags with class 'type-icon' inside tables with class 'vitals-table'
        type_tags = soup.select(".vitals-table a.type-icon")
        # Combine the types into a single comma-separated string to make it easier to store database field because pokemon can have more than 1 type
        types = ", ".join(t.text for t in type_tags)

        # --- Set Default Values for the Stats for: HP, Attack, Defense ---
        stat_map = {"hp": 0, "attack": 0, "defense": 0}  # Default values

        # Locate the header for the 'Base stats' section in the downloaded HTML for the pokemon page
        base_stats_header = soup.find("h2", string=re.compile("Base stats", re.I))
        if base_stats_header:
            # Find the next table in the HTML with class 'vitals-table' which is after the header
            base_stats_table = base_stats_header.find_next("table", class_="vitals-table")
            if base_stats_table:
                # Iterate over each row in the stats table
                for row in base_stats_table.find_all("tr"):
                    th = row.find("th")  # Grab Stat name (e.g., HP, Attack, Defense)
                    td = row.find("td")  # Grab Stat value
                    if th and td:
                        label = th.text.strip().lower()  # Convert label to lowercase
                        value = re.search(r"\d+", td.text.strip())  # Extract number from text
                        if label in stat_map and value:
                            stat_map[label] = int(value.group())  # Save the numeric value

        # --- Get Abilities ---
        abilities = "Unknown"  # Set Default value
        ab_row = soup.find("th", string="Abilities")  # Look for 'Abilities' header in the HTML of the webpage
        if ab_row:
            ab_cell = ab_row.find_next_sibling("td")  # Find corresponding stat value aka <td> with ability values
            # Join multiple abilities if present to make it easier to store database field
            abilities = ", ".join(ab_cell.stripped_strings)

        # --- Return the final structured data ---
        return {
            "name": name.capitalize(),
            "types": types,
            "hp": stat_map["hp"],
            "attack": stat_map["attack"],
            "defense": stat_map["defense"],
            "abilities": abilities
        }

    except Exception as e:
        # Print error if parsing fails
        print("Error parsing HTML:", e)
        return None

	
