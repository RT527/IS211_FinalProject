Overview

This is a Flask web application that allows users to log in, search for books using the Google Books API, and save them to a personal catalogue. Books are stored in a SQLite database and displayed in a themed dashboard. Users can also delete entries.

Features

Multi-user login (users stored in the database)

Add books by ISBN using Google Books API

Display title, author, pages, and rating (N/A if missing)

Delete book entries via button

Persistent storage using SQLite + SQLAlchemy

Custom “top-secret” themed UI