# Article-Search-App
A program that does auto search and come up with top articles around internet. No Ai. Modern and cool GUI with tkinter

The Article Search App is a desktop application built with Python and Tkinter that allows users to search for academic research papers from the arXiv database. 

How the Program Works
1. Importing Libraries

The application imports several Python libraries, each responsible for a different part of the program:

Library	Purpose
tkinter	Creates the graphical interface
messagebox	Displays warning messages
ttk	Styles widgets like the scrollbar
urllib.request	Downloads data from arXiv
urllib.parse	Encodes user search queries into URLs
xml.etree.ElementTree	Parses the XML response from arXiv
threading	Runs searches without freezing the interface
webbrowser	Opens article links in the user's default browser

These imports provide all the functionality needed for the application.
