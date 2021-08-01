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
        # If the input data has 6 elements, there is an ID.
        if (len(data) == 6):
            self.id = data[0]
            self.name = data[1].strip()
            self.year = data[2]
            self.rating = data[3].strip()
            self.runtime = data[4]
            self.genre = data[5].strip()
        # Otherwise, it does not contain an ID.
        else:
            self.id = -1
            self.name = data[0].strip()
            self.year = data[1]
            self.rating = data[2].strip()
            self.runtime = data[3]
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
# Create the movies table if it doesn't exist yet
c.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, year INTEGER NOT NULL, rating TEXT NOT NULL, runtime INTEGER NOT NULL, genre TEXT NOT NULL);")
db.commit()

# MAIN MENU
# Create the main menu.
while True:
    mainMenuOptions = {'Search your library': 'search', 'Add a movie to your library': 'add', 'Remove a movie from your library': 'remove',
                       'Update a movie already in your library': 'update', 'View all the movies in your library': 'view', 'Exit Movie Manager': 'exit'}
    mainMenuChoice = mainMenuOptions[eg.buttonbox('Welcome to Movie Manager!\nPlease choose an option.',
                                                  'Movie Manager - Main Menu', list(mainMenuOptions.keys()))]
    if mainMenuChoice == 'search':
        # Search for a movie.
        while True:
            # STEP 1 - GET SEARCH TERMS
            # Present a window with search options.
            # The user can search by any field.
            fields = {'Movie Title:': 'name', 'Release Year:': 'year',
                      'Rating:': 'rating', 'Length (minutes):': 'runtime', 'Genre:': 'genre'}
            search = eg.multenterbox(
                "Enter your search conditions and press OK to search.\n\nIf you fill out multiple fields, a movie must match all of them.\nFields are not case-sensitive.",
                "Movie Manager - Search Library",
                list(fields.keys()))
            # If search equals None, the user has cancelled the search.
            if (search == None):
                break
            # If the user has not cancelled the search, perform the search.
            # STEP 2 - CONSTRUCT A QUERY STRING
            else:
                query = "SELECT * from movies "
                # First, construct the query by concatenating the search terms.
                # For each field that has been filled, add it to the query:
                needsAnd = False
                for index, data in enumerate(search):
                    # Get the field associated with the search term.
                    field = list(fields.values())[index]
                    # If it's blank, skip it.
                    if (data.strip() == ""):
                        continue
                    else:
                        # Otherwise, concatenate the search term to the query.
                        if (needsAnd == True):
                            # If this isn't the first search term, add an 'AND' to the query.
                            query += f" AND {field} LIKE '%{data.strip()}%'"
                        else:
                            query += f" WHERE {field} LIKE '%{data.strip()}%'"
                            needsAnd = True
            # STEP 3 - PERFORM SEARCH
                # Now that we have a constructed query, execute it and display the results.
                rawResults = c.execute(query).fetchall()
            # STEP 4 - DISPLAY RESULTS
                # Convert the fetched data (list of tuples) to a list of Movie objects for easier handling.
                results = []
                for result in rawResults:
                    results.append(Movie(result))
                # Finally, display the list of movies in a textbox.
                eg.textbox(f"Found {len(rawResults)} movies.\nPress OK to return to the search menu.",
                           "Movie Manager - Search Library - Results",
                           # Use a list comprehension to create the formatted output.
                           [(result.string() + "\n") for result in results])
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
                        "INSERT INTO movies VALUES (null,?,?,?,?,?)", rawNewMovie)
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
        # Get a complete list of all the movies in the database.
        rawMovies = c.execute("SELECT * FROM movies").fetchall()
        # Convert the fetched data (list of tuples) to a list of Movie objects for easier handling.
        movies = []
        for movie in rawMovies:
            movies.append(Movie(movie))
        # Finally, display the list of movies in a textbox.
        eg.textbox(f"There are {len(rawMovies)} movies stored in the database.\nPress OK to return to the main menu.",
                   "Movie Manager - View Library",
                   # Use a list comprehension to create the formatted output.
                   [(movie.string() + "\n") for movie in movies])
    elif mainMenuChoice == 'exit':
        # Exit the program.
        if (eg.buttonbox('Are you sure you want to exit?', 'Movie Manager - Exit', ('Yes', 'No'))) == 'Yes':
            quit()
        else:
            pass
