# MOVIE MANAGER for Python
# By Conor Eager
# Developed for Computer Science NCEA Level 2 - AS91892 & AS91897
# © (copyright) Conor Eager, 2021. All rights reserved.

# IMPORTS
# Import EasyGUI for GUI
import easygui as eg
# Import sqlite3 for databases
import sqlite3 as sql

# FUNCTIONS


def isInteger(value):
    # Check if value is an integer
    try:
        int(value)
        return True
    except ValueError:
        return False

# CLASSES


class Movie:
    def __init__(self, data):
        # Initialise a new movie from a list.
        self.name = data[0].strip()
        self.year = data[1].strip()
        self.rating = data[2].strip()
        self.runtime = data[3].strip()
        self.genre = data[4].strip()

    def export(self):
        # Export the movie data to a list.
        return [self.name, self.year, self.rating, self.runtime, self.genre]

    def string(self):
        # Returns a formatted version of the movie data.
        return f"'{self.name}' ({self.year})  - {self.genre}, {self.runtime} mins, {self.rating}"

    def validate(self):
        # Validate the movie data. Return false if invalid, true if valid.
        if (self.name == ""):
            eg.msgbox(
                "Error: the movie title must not be blank.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (self.year == ""):
            eg.msgbox(
                "Error: the movie year must not be blank.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (isInteger(self.year) == False):
            eg.msgbox(
                "Error: the movie year must be an integer.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (self.rating == ""):
            eg.msgbox(
                "Error: the movie rating must not be blank.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (self.runtime == ""):
            eg.msgbox(
                "Error: the movie runtime must not be blank.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (isInteger(self.runtime) == False):
            eg.msgbox(
                "Error: the movie runtime must be an integer.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        elif (self.genre == ""):
            eg.msgbox(
                "Error: the movie genre must not be blank.",
                "Movie Manager - Add Movie",
                "Try Again")
            return False
        else:
            return True


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
    mainMenuChoice = mainMenuOptions[eg.buttonbox('Welcome to Movie Manager!\nPlease choose an option.',
                                                  'Movie Manager - Main Menu', list(mainMenuOptions.keys()))]
    if mainMenuChoice == 'search':
        # Search for a movie.
        pass
    elif mainMenuChoice == 'add':
        # Add a movie to the database.
        # Create a blank record to hold the new data:
        # [name, year, rating, runtime, genre]
        rawNewMovie = ["", 1990, "", 0, ""]
        while True:
            rawNewMovie = eg.multenterbox(
                "Enter the details for the new movie:",
                "Movie Manager - Add Movie",
                ["Movie Title:", "Release Year:", "Rating:",
                    "Length (minutes):", "Genre:"],
                rawNewMovie)
            if (rawNewMovie == None):
                # The user pressed Cancel, so go back to the main menu.
                break
            else:
                # Otherwise, process the data and check for any errors.
                newMovie = Movie(rawNewMovie)
                if (newMovie.validate() == True):
                    # If all checks have passed, then create the record and add it:
                    c.execute(
                        "INSERT INTO movies VALUES (?,?,?,?,?)", rawNewMovie)
                    db.commit()
                    # Notify the user:
                    eg.msgbox("Movie added successfully!",
                              "Movie Manager - Add Movie", "Back to Menu")
                    break
                else:
                    # Checks failed, so notify the user and try again.
                    continue

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
