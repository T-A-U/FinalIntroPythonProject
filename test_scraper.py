#Scraper file was initially returning zeros for HP, attack, and defense so I wrote this to test the output data in the database (via the terminal)

from scraper import scrape_pokemon_data

result = scrape_pokemon_data("Raichu")
print(result)
