# Lightweight Deadlock App
This is an app that pulls from the deadlock API and shows various stats about the game and opponents. 

# The Problem
The main goal with this project is to create an app to easily look up opponents and see their match history, rank, characters they play, and weaknesses in one easily digestible page.

# How it Works
The user will input the player ID of whatever player they want to look up. This will work a thread in the background to request match history data from the Deadlock API servers. 
The fetched data will be parsed and put into a readable page for the user.

# Tech Stack
PySide6, requests, QThread, Deadlock API

# Setup Instructions
This is to be done.

# MVP Roadmap
Initial commit with basic project files, README, starter file setup - [x]\
Write the API fetching code, taking Steam ID to retrieve match history and data - [x]\
Basic error handling, terminal testing - [x]\
Minimal window, contains search bar and button, with a result label that prints API output - [x]\
Moves API calls onto a worker thread to allow more flexibility with the frontend during the fetching process - [x]\
Core viewing with basic profile summary: top heroes, recent matches list. Readable frontend - [ ]\
Implement caching and front-end error messages for repeat or failed lookups - [ ]\
Package the program, fix up REAME - [ ]\
Official release on Github - [ ]


# Video demo
This is to be done.


# Extra features to Add Later

Possible Update Features:
Optional API key setting\
Steam vanity name and profile URL input\
Charts and graphs\
Saved or favorite players\
Auto-updater and installer (?)\
Discord bot sharing the same API script
