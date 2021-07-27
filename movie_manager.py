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
