# MOVIE MANAGER for Python
# By Conor Eager
# Developed for Computer Science NCEA Level 2 - AS91892 & AS91897
# © (copyright) Conor Eager, 2021. All rights reserved.

# IMPORTS
# Import EasyGUI for GUI
from tkinter.constants import S
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


def search(message, purpose):
    # Search the library and return the results.
    # STEP 1 - GET SEARCH TERMS
    # Present a window with search options.
    # The user can search by any field.
    fields = {'Movie Title:': 'name', 'Release Year:': 'year',
              'Rating:': 'rating', 'Length (minutes):': 'runtime', 'Genre:': 'genre'}
    search = eg.multenterbox(
        f"{message}\n\nEnter your search conditions and press OK to search.\n\nName and Genre will be matched at any point. Rating, Year and Length will be matched from the start.\nIf you fill out multiple fields, a movie must match all of them.\nFields are not case-sensitive.",
        f"Movie Manager - {purpose}",
        list(fields.keys()))
    # If search equals None, the user has cancelled the search.
    if (search == None):
        return None
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
                # If the field is Rating, Year or Length, match from the start only.
                if (field == "year" or field == "runtime" or field == "rating"):
                    if (needsAnd == True):
                        # If this isn't the first search term, add an 'AND' to the query.
                        query += f" AND {field} LIKE '{data.strip()}%'"
                    else:
                        query += f" WHERE {field} LIKE '{data.strip()}%'"
                        needsAnd = True
                else:
                    # Otherwise, match anywhere.
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
        # If there were no results, display a message and return to the search menu.
        if (len(rawResults) == 0):
            return []
        # Otherwise...
        else:
            # Convert the fetched data (list of tuples) to a list of Movie objects for easier handling.
            results = []
            for result in rawResults:
                results.append(Movie(result))
            return results


def selectMovie(results, message, purpose):
    # Allow the user to select a movie from a list of Movie objects, and return the selected movie.
    # This is more difficult than it sounds, because EasyGUI returns the STRING that was selected, not the object itself.
    selectionList = [(result.string() + "\n") for result in results]
    selection = eg.choicebox(f"Found {len(results)} movies.\n{message}",
                             f"Movie Manager - {purpose}",
                             selectionList)
    if (selection == None):
        return None
    else:
        # Get the movie by reverse-searching the list for the index, and getting the Movie object at that index.
        # Yes, it's a mess, but it works.
        return results[selectionList.index(selection)]

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
        return f"'{self.name}' ({self.year}) - {self.genre}, {self.runtime} mins, {self.rating}"

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
                       'Update a movie already in your library': 'update', 'View all the movies in your library': 'view', 'Pick a random movie': 'random', 'Exit Movie Manager': 'exit'}
    mainMenuChoice = mainMenuOptions[eg.buttonbox('Welcome to Movie Manager!\nPlease choose an option.',
                                                  'Movie Manager - Main Menu', list(mainMenuOptions.keys()))]
    if mainMenuChoice == 'search':
        # Search for a movie.
        while True:
            results = search("Search your movie library.", "Search Library")
            # If none, cancel the search.
            if (results == None):
                break
            # If there are no results, display a message and return to the search menu.
            if (len(results) == 0):
                eg.msgbox("No results found.\nCheck your search terms and try again.",
                          "Movie Manager - Search Library",
                          "Try Again")
                continue
            # Otherwise, display the returned list of movies in a textbox.
            else:
                eg.textbox(f"Found {len(results)} movies.\nPress OK to return to the search menu.",
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
        results = search(
            "Search your movie library for the movie you want to remove, or leave all fields blank to display all.", "Remove Movie")
        # If none, cancel.
        if (results == None):
            continue
        # If there are no results, display a message and return to the search menu.
        elif (len(results) == 0):
            eg.msgbox("No movies found.\nCheck your search terms and try again.",
                      "Movie Manager - Remove Movie",
                      "Try Again")
            continue
        # Otherwise, display the returned list of movies in a choicebox for the user to select the correct one.
        else:
            selection = selectMovie(
                results, "Select the movie you would like to remove and press OK.", "Remove Movie")
            if (selection == None):
                continue
            # Get confirmation from the user.
            if (eg.buttonbox(f"Are you sure you want to remove this movie from your library?\nThis cannot be undone!\n\n{selection.string()}",
                             "Movie Manager - Remove Movie",
                             ["Yes, remove the movie", "No, do not remove the movie"]) == "Yes, remove the movie"):
                # Remove the record:
                c.execute(f"DELETE FROM movies WHERE id={selection.id}")
                db.commit()
                # Notify the user:
                eg.msgbox("Movie removed successfully!",
                          "Movie Manager - Remove Movie",
                          "Back to Menu")
                continue
            else:
                eg.msgbox("Movie not removed.",
                          "Movie Manager - Remove Movie",
                          "Back to Menu")
    elif mainMenuChoice == 'update':
        # Update a movie.
        results = search(
            "Search your movie library for the movie you want to update, or leave all fields blank to display all.", "Update Movie")
        # If none, cancel.
        if (results == None):
            continue
        # If there are no results, display a message and return to the search menu.
        elif (len(results) == 0):
            eg.msgbox("No movies found.\nCheck your search terms and try again.",
                      "Movie Manager - Update Movie",
                      "Try Again")
            continue
        # Otherwise, display the returned list of movies in a choicebox for the user to select the correct one.
        else:
            oldMovie = selectMovie(
                results, "Select the movie you would like to update and press OK.", "Update Movie")
            if (oldMovie == None):
                continue
            # Create a new movie object to hold the updated data:
            newMovie = oldMovie
            rawNewMovie = newMovie.export()
            # Get the changes:
            while True:
                rawNewMovie = eg.multenterbox(
                    "Enter the details for the updated movie:",
                    "Movie Manager - Update Movie",
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
                        # If all checks have passed, then update it:
                        # Get confirmation from the user.
                        if (eg.buttonbox(f"Are you sure you want to update this movie?\nThis cannot be undone!\n\nBEFORE:\n{oldMovie.string()}\n\nAFTER:\n{newMovie.string()}",
                                         "Movie Manager - Update Movie",
                                         ["Yes, update the movie", "No, do not update the movie"]) == "Yes, update the movie"):
                            # Update the record:
                            c.execute(
                                f"UPDATE movies SET name = ?, year = ?, rating = ?, runtime = ?, genre = ? WHERE id={oldMovie.id};", newMovie.export())
                            db.commit()
                            # Notify the user:
                            eg.msgbox("Movie updated successfully!",
                                      "Movie Manager - Update Movie",
                                      "Back to Menu")
                            break
                        else:
                            eg.msgbox("Movie not updated.",
                                      "Movie Manager - Update Movie",
                                      "Back to Menu")
                            break
                    else:
                        # Checks failed, so notify the user and try again.
                        continue
            if (rawNewMovie == None):
                continue
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
    elif mainMenuChoice == 'random':
        movie = c.execute(
            "SELECT * FROM movies ORDER BY RANDOM() LIMIT 1").fetchall()
        if (len(movie) == 0):
            # There are no movies in the database!
            eg.msgbox("There are no movies in your library!\nClick 'Add a movie to your library' on the Main Menu to add one.",
                      "Movie Manager - Random Movie",
                      "Back to Menu")
        else:
            movie = Movie(movie[0])
            eg.msgbox(f"Your random movie is...\n\n{movie.string()}",
                      "Movie Manager - Random Movie",
                      "OK")
    elif mainMenuChoice == 'exit':
        # Exit the program.
        if (eg.buttonbox("Are you sure you want to exit?\nYou won't lose your movie library.", "Movie Manager - Exit", ("Yes, exit", "No, do not exit"))) == "Yes, exit":
            quit()
        else:
            pass
