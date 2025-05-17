# Pokémon Info App
# Author: Tau Adegun
# Date: May 2025
# Description: A Python app with a GUI that shows Pokémon info using a SqLite database and web scraping.


import tkinter as tk  # Used to create the GUI window
from tkinter import messagebox, PhotoImage  # Used to show error, pop-up messages, and main pokemon logo image
from db import init_db, get_pokemon_from_db, save_pokemon_to_db  # Functions to work with the database
from scraper import scrape_pokemon_data  # Function to get data from the website

def start_app():
    """
    This function starts the whole GUI app.
    It sets up the database and the layout of the window.
    """
    init_db()  # Make sure database and table are ready

    def search():
        """
        This function is called when the user clicks the Search button.
        It checks if the Pokémon is in the database.
        If not, it will try to get info from the website.
        """
        name = entry.get().strip()  # Get what the user typed
        if name == "":
            messagebox.showerror("Error", "Please enter a Pokémon name.")
            return

        data = get_pokemon_from_db(name)  # Try to find Pokémon in the database

        if not data:
            data_dict = scrape_pokemon_data(name)  # Try to scrape from the website
            if data_dict:
                save_pokemon_to_db(data_dict)  # Save new info into the database
                data = (
                    data_dict['name'],
                    data_dict['types'],
                    data_dict['hp'],
                    data_dict['attack'],
                    data_dict['defense'],
                    data_dict['abilities']
                )
            else:
                messagebox.showinfo(
                    "Not Found",
                    "Sorry, we couldn’t find data for this Pokémon. Please check the spelling or try another."
                )
                return

        show_data(data)  # Show the result on screen

    def show_data(info):
        """
        This function shows the Pokémon info on the screen.
        """
        output.delete("1.0", tk.END)  # Clear previous text
        labels = ["Name", "Type(s)", "HP", "Attack", "Defense", "Abilities"]
        for label, value in zip(labels, info):
            output.insert(tk.END, f"{label}: {value}\n")

    # Set up the main window
    window = tk.Tk() #Standard window setup code
    window.title("Pokémon Info App")#Give the app a title
    window.configure(bg="#FFCC00")  # Pokémon-style background (like Pikachu)

    # Load and display logo image
    try:
        logo_image = PhotoImage(file="pokemon-logo.png")  # Found in stack overflow as a fix to get imge to show up # Show logo which is saved in the repository (or folder if local) and resize image to 1/8 it's original size (originally huge)
        logo_image = logo_image.subsample(8, 8)  # Resize image to about 1/8x smaller than original big size
        logo_label = tk.Label(window, image=logo_image, bg="#FFCC00") #Give the label a color etc
        logo_label.image = logo_image  # Keep a reference of the image just incase you need it
        logo_label.pack(pady=10)#Place the logo vertically within the window using the .pack() layout manager and add 10 pixels of vertical padding above and below the image using pady=10
    except Exception as e: #If something goes wrong, print the below error
        print("Could not load logo image:", e)

    # Add label and input box
    tk.Label(window, text="WELCOME TO THE POKEMON POKEDEX!", bg="#FFCC00", font=("Arial", 12, "bold")).pack(pady=5) #Create label for user input box
    tk.Label(window, text="Enter the name of your favorite pokemon, press 'Search'", bg="#FFCC00", font=("Arial", 12, "bold")).pack(pady=5)
    entry = tk.Entry(window) #Code for Actual inut box in Tkinter
    entry.pack(pady=5)#Aligns vertical using .pack() and adds 5 pixels above and below

    # Add search button
    tk.Button(window, text="Search", command=search, bg="#FF0000", fg="blue", font=("Arial", 10, "bold")).pack(pady=5) #Design the Search button with blue words fg="blue"

    # Add a text area to show results
    tk.Label(window, text="Pokemon Information displayed below:", bg="#FFCC00", font=("Arial", 12, "bold")).pack(pady=5)
    output = tk.Text(window, height=10, width=50, bg="white", fg="blue") #Design the output section with blue words fg="blue" where pokemon info will go
    output.pack(pady=10)#Aligns vertical using .pack() and adds 10 pixels above and below

    window.mainloop()  # Start the GUI loop and keep the window open
