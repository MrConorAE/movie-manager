# MOVIE MANAGER for Python
# By Conor Eager
# Developed for Computer Science NCEA Level 2 - AS91892 & AS91897
# © (copyright) Conor Eager, 2021. All rights reserved.

# IMPORTS
# Import EasyGUI for GUI
import easygui as eg
# Import sqlite3 for databases
import sqlite3 as sql

# INITIALISATION
# Initialise the connection to the database.
db = sql.connect('movies.db')
# Initialise the cursor.
c = db.cursor()

# MAIN MENU
# Create the main menu.
while True:
    mainMenuOptions = {'Search your library': 'search', 'Add a movie': 'add', 'Remove a movie': 'remove',
                       'Update a movie': 'update', 'View your library': 'view', 'Exit': 'exit'}
    mainMenuChoice = eg.buttonbox('Welcome to Movie Manager!\nPlease choose an option.',
                                  'Movie Manager - Main Menu', list(mainMenuOptions.keys()))
    if mainMenuChoice == 'search':
        # Search for a movie.
        pass
    elif mainMenuChoice == 'add':
        # Add a movie to the database.
        pass
    elif mainMenuChoice == 'remove':
        # Remove a movie.
        pass
    elif mainMenuChoice == 'update':
        # Update a movie.
        pass
    elif mainMenuChoice == 'view':
        # View the movies in the database.
        pass
    elif mainMenuChoice == 'exit':
        # Exit the program.
        if (eg.buttonbox('Are you sure you want to exit?', 'Movie Manager - Exit', ('Yes', 'No'))) == 'Yes':
            quit()
        else:
            pass
