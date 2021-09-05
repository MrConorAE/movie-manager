# MOVIE MANAGER for Python
# By Conor Eager
# Developed for Computer Science NCEA Level 2 - AS91892 & AS91897
# © (copyright) Conor Eager, 2021. All rights reserved.
# Up-to-date versions available for download at https://github.com/mrconorae/movie-manager

# IMPORTS
# Import EasyGUI for GUI
import easygui as eg
# Import sqlite3 for databases
import sqlite3 as sql
# Import pickle for exporting and importing compressed dumps
import pickle
# Import csv for reading and writing CSV files
import csv

# FUNCTIONS


def isInteger(value):
    """Check if the passed value is an integer.

    Args:
        value (Any): The value to test.

    Returns:
        Literal[True, False]: True if the value is an integer, False if it isn't.
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def search(message, purpose):
    """Open a window where the user can input search terms to search the database, and return the results in Movie format.

    Args:
        message (String): A message to display to the user, explaining what they are searching for.
        purpose (String): A string to identify the purpose of the search ("Remove Movie" or "Search Library").

    Returns:
        List[Movie]: A list of Movie objects representing the results, an empty array if there were no results or None if the search was cancelled.
    """
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
    """Allow the user to select a movie from a list of Movie objects (e.g. from a search).

    Args:
        results (List[Movie]): The list of options, as Movie objects.
        message (String): A message explaining to the user what they are selecting.
        purpose (String): A string to identify the purpose of the search ("Remove Movie" or "Search Library").

    Returns:
        Movie: The movie that was selected.
    """
    # Allow the user to select a movie from a list of Movie objects, and return the selected movie.
    # This is more difficult than it sounds, because EasyGUI returns the STRING that was selected, not the object itself.
    selectionList = [(result.string(True) + "\n") for result in results]
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
    """This class represents a movie.
    """

    def __init__(self, data):
        """Create a new Movie object.

        Args:
            data (List): The required data to create a new Movie object.
            Format: [?]ID (optional), [0]Name, [1]Year, [2]Rating, [3]Runtime, [4]Genre
        """
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
        """Export the movie as a list of values. The opposite of __init__().

        Returns:
            List: The movie data.
        """
        return [self.name, self.year, self.rating, self.runtime, self.genre]

    def string(self, table):
        """Returns a formatted string representing the movie. Used for displaying the movie to the user.

        Returns:
            String: The movie data, formatted as a string.
        """
        if (table == True):
            return f"{self.name:<40}  {self.year:<4}  {self.genre:<25}  {self.runtime:>8} mins   {self.rating}"
        else:
            return f"'{self.name}' ({self.year}) - {self.genre}, {self.runtime} mins, {self.rating}"

    def validate(self):
        """Validate the movie data (check that all fields are filled and valid format).

        Returns:
            Literal[True, False]: True if checks passed, False otherwise.
        """
        errors = ""
        if (self.name == ""):
            errors += "- The movie title must not be blank.\n"
        if (self.year == ""):
            errors += "- The movie year must not be blank.\n"
        if (isInteger(self.year) == False):
            errors += "- The movie year must be an integer.\n"
        if (self.rating == ""):
            errors += "- The movie rating must not be blank.\n"
        if (self.runtime == ""):
            errors += "- The movie runtime must not be blank.\n"
        if (isInteger(self.runtime) == False):
            errors += "- The movie runtime must be an integer.\n"
        if (self.genre == ""):
            errors += "- The movie genre must not be blank.\n"

        # Now show the user the errors (if any) and return whether or not the data is valid.
        if (errors == ""):
            return True
        else:
            eg.msgbox(
                f"The movie is invalid and cannot be added. Please fix the following errors:\n\n{errors}",
                "Movie Manager - Add Movie",
                "Try Again")
            return False


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
                       'Update a movie already in your library': 'update', 'View all the movies in your library': 'view', 'Import/Export your library': 'importexport', 'Pick a random movie': 'random', 'Exit Movie Manager': 'exit'}
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
                eg.codebox(f"Found {len(results)} movies.\nPress OK to return to the search menu.",
                           "Movie Manager - Search Library - Results",
                           # Use a list comprehension to create the formatted output.
                           [(result.string(True) + "\n") for result in results])
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
            if (eg.buttonbox(f"Are you sure you want to remove this movie from your library?\nThis cannot be undone!\n\n{selection.string(False)}",
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
                        if (eg.buttonbox(f"Are you sure you want to update this movie?\nThis cannot be undone!\n\nBEFORE:\n{oldMovie.string(False)}\n\nAFTER:\n{newMovie.string(False)}",
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
        # Ask the user how they would like the results sorted:
        sortoptions = {"Title (default)": "name", "Release Year": "year",
                       "Rating": "rating", "Runtime": "runtime", "Genre": "genre", "Cancel": None}
        sortby = sortoptions[eg.buttonbox("How would you like to sort the results?",
                                          "Movie Manager - View Library",
                                          list(sortoptions.keys()))]
        # If the user presses Cancel, exit:
        if (sortby == None):
            continue
        # Get the list of movies in the database, sorted by the user's preference:
        rawMovies = c.execute(
            f"SELECT * FROM movies ORDER BY {sortby}").fetchall()
        # Convert the fetched data (list of tuples) to a list of Movie objects for easier handling.
        movies = []
        for movie in rawMovies:
            movies.append(Movie(movie))
        # Finally, display the list of movies in a textbox.
        eg.codebox(f"There are {len(rawMovies)} movies stored in the database.\nPress OK to return to the main menu.",
                   "Movie Manager - View Library",
                   # Use a list comprehension to create the formatted output.
                   [(movie.string(True) + "\n") for movie in movies])
    elif mainMenuChoice == 'importexport':
        # Allow the user to import or export their library as a .csv or pickle dump.
        mode = eg.buttonbox("What would you like to do?\n\nImport and Add - import movies and add them to the library, leaving existing movies alone\nImport and Replace - import movies and replace the library with the imported set, deleting all the existing movies\nExport - export your entire library", "Movie Manager - Import/Export - Step 1/3",
                            ["Import and Add", "Import and Replace", "Export", "Cancel"])
        if mode == "Cancel":
            continue
        filetype = eg.buttonbox("What file format?\n\n.csv - readable by other applications like Excel, but larger\n.mvd - not readable by other applications, but much smaller", "Movie Manager - Import/Export - Step 2/3",
                                [".csv", ".mvd", "Cancel"])
        if filetype == "Cancel":
            continue
        # Import and Add and Import and Replace: get the movies and append them to the database.
        if mode == "Import and Add" or mode == "Import and Replace":
            # Open a file picker for the user to select a file to import.
            if (filetype == ".csv"):
                try:
                    filename = eg.fileopenbox(
                        "Select a .csv file to import:", "Movie Manager - Import/Export - Step 3/3", "*.csv", [["*.csv", "CSV files"]])
                    # If the user pressed Cancel, exit
                    if filename == None:
                        continue
                    with open(filename, "rt", newline="") as f:
                        reader = csv.reader(f)
                        # Process the CSV data:
                        loadedMovies = []
                        for row in reader:
                            loadedMovies.append(
                                Movie(row))
                    # Get confirmation before importing.
                    if (eg.buttonbox(f"Replace current library with {len(loadedMovies)} movies from {filename}?", "Movie Manager - Import/Export - Confirmation", ["Yes, replace", "No, do not replace"]) == "Yes, replace"):
                        # If they agree, import the movies.
                        if mode == "Import and Replace":
                            c.execute("DELETE FROM movies")
                        c.executemany(
                            "INSERT INTO movies VALUES (null, ?, ?, ?, ?, ?)", [movie.export() for movie in loadedMovies])
                        db.commit()
                        # Notify the user:
                        eg.msgbox("Movies imported successfully!",
                                  "Movie Manager - Import/Export - Complete",
                                  "Back to Menu")
                        continue
                except Exception as e:
                    eg.msgbox(f"Error: could not import. Check that this is a valid .csv file, and that you have permissions to read the file.\n\n{e}",
                              "Movie Manager - Import/Export - Error", "Back to Menu")
                    continue
            elif (filetype == ".mvd"):
                try:
                    filename = eg.fileopenbox(
                        "Select a .mvd file to import:", "Movie Manager - Import/Export - Step 3/3", "*.mvd", [["*.mvd", "MVD files"]])
                    # If the user pressed Cancel, exit
                    if filename == None:
                        continue
                    with open(filename, "rb") as f:
                        loadedMovies = pickle.load(f)
                    # Get confirmation before importing.
                    if (eg.buttonbox(f"Replace current library with {len(loadedMovies)} movies from {filename}?", "Movie Manager - Import/Export - Confirmation", ["Yes, replace", "No, do not replace"]) == "Yes, replace"):
                        # If they agree, import the movies.
                        c.execute("DELETE FROM movies")
                        c.executemany(
                            "INSERT INTO movies VALUES (null, ?, ?, ?, ?, ?)", [movie.export() for movie in loadedMovies])
                        db.commit()
                        # Notify the user:
                        eg.msgbox("Movies imported successfully!",
                                  "Movie Manager - Import/Export - Complete",
                                  "Back to Menu")
                        continue
                except Exception as e:
                    eg.msgbox(f"Error: could not import. Check that this is a valid .mvd file, and that you have permissions to read the file.\n\n{e}",
                              "Movie Manager - Import/Export - Error", "Back to Menu")
                    continue
        # Export: get the movies and export them to a file.
        elif mode == "Export":
            # Open a file picker for the user to select a file to export.
            if (filetype == ".csv"):
                try:
                    filename = eg.filesavebox(
                        "Select a .csv file to save to:", "Movie Manager - Import/Export - Step 3/3", "*.csv", [["*.csv", "CSV files"]])
                    # If the user pressed Cancel, exit
                    if filename == None:
                        continue
                    loadedMovies = c.execute(
                        "SELECT * FROM movies").fetchall()
                    # Get confirmation before exporting.
                    if (eg.buttonbox(f"Export {len(loadedMovies)} movies to {filename}?", "Movie Manager - Import/Export - Confirmation", ["Yes, export", "No, do not export"]) == "Yes, export"):
                        # If they agree, export the movies.
                        with open(filename, "wt", newline="") as f:
                            writer = csv.writer(f)
                            # Process the CSV data:
                            # Exclude the ID, because it'll cause problems when importing:
                            for movie in loadedMovies:
                                writer.writerow(movie[1:])
                        # Notify the user:
                        eg.msgbox("Movies exported successfully!",
                                  "Movie Manager - Import/Export - Complete",
                                  "Back to Menu")
                        continue
                except Exception as e:
                    eg.msgbox(f"Error: could not export. Check that you have permissions to write the file.\n\n{e}",
                              "Movie Manager - Import/Export - Error", "Back to Menu")
                    continue
            elif (filetype == ".mvd"):
                try:
                    filename = eg.filesavebox(
                        "Select a .mvd file to save to:", "Movie Manager - Import/Export - Step 3/3", "*.mvd", [["*.mvd", "MVD files"]])
                    # If the user pressed Cancel, exit
                    if filename == None:
                        continue
                    loadedMovies = c.execute("SELECT * FROM movies").fetchall()
                    # Get confirmation before exporting.
                    if (eg.buttonbox(f"Export {len(loadedMovies)} movies to {filename}?", "Movie Manager - Import/Export - Confirmation", ["Yes, export", "No, do not export"]) == "Yes, export"):
                        # If they agree, export the movies.
                        with open(filename, "wb") as f:
                            pickle.dump(loadedMovies, f)
                        # Notify the user:
                        eg.msgbox("Movies exported successfully!",
                                  "Movie Manager - Import/Export - Complete",
                                  "Back to Menu")
                        continue
                except Exception as e:
                    eg.msgbox(f"Error: could not export. Check that this is a valid .mvd file, and that you have permissions to read the file.\n\n{e}",
                              "Movie Manager - Import/Export - Error", "Back to Menu")
                    continue
    elif mainMenuChoice == 'random':
        # Choose a random movie from the library.
        while True:
            movie = c.execute(
                "SELECT * FROM movies ORDER BY RANDOM() LIMIT 1").fetchall()
            if (len(movie) == 0):
                # There are no movies in the database!
                eg.msgbox("There are no movies in your library!\nClick 'Add a movie to your library' on the Main Menu to add one.",
                          "Movie Manager - Random Movie",
                          "Back to Menu")
                break
            else:
                movie = Movie(movie[0])
                if (eg.buttonbox(f"Your random movie is...\n\n{movie.string(False)}",
                                 "Movie Manager - Random Movie",
                                 ["Back to Menu", "Pick Again"]) == "Back to Menu"):
                    break
                else:
                    continue
    elif mainMenuChoice == 'exit':
        # Exit the program.
        quit()
