# Lightweight-Deadlock-App
This is an app that pulls from the deadlock API and shows various stats about the game and opponents. 

The main goal with this project is to create an app to easily look up opponents and see what their rank, chracters they play, and weaknesses in one easily digestible page.

A more secondary goal is to create an easy place to lookup builds for characters or even randomly generate a build for fun.

In the MVP:
Search box for an account ID, with a Search button
Profile summary (rank/MMR and overall stats)
Top heroes in a simple table
Recent match history list (hero, result, KDA)
Loading indicator and readable error messages(player not found, API down, rate-limited)
Background threading so the window doesn't freeze
Simple local cache so repeat lookups are quick

Possible Update Features:
Optional API key setting
Steam vanity name and profile URL input
Charts and graphs
Saved or favorite players
Auto-updater and installer (?)
Discord bot sharing the same API script
