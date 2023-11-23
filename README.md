# ProjetInfo2A
Projet Informatique 2A ENSAI (Sujet 8 : Velib' Hunter)

# Purpose
This application is meant to offer several functionalities to their users in order to manage their access to the Velib' system database.

- For a regular user, he can find the nearest station with available bikes with functionnalite-1 by entering his position - a position that could be written as a usual address instead of geographic coordinates thanks to the use of Etalab API ;
- For a statistical purpose, the Velib' system managers could get access to the least-frequented station on a specific period of time he enters in functionnalite-2 ;
- They could also get access the least-frequented Paris borough on a specific period of time he enters in functionnalite-3. 

# Example

First functionality:
 - When searching for the nearest station with at least 1 available bike, the user would input /fonctionnalite-1/?user_location=lat,lon . lat being the current user's latitude and lon being the current user's longitude. Note that, if the user does not specify anything and just input /fonctionnalite-1 , the API will return the nearest station to these coordinates 48.8563199, 2.31345367

Second functionality:
 - When looking for the least frequented station on a period of time, the user would input /fonctionnalite-2/?date_debut=date1&date_fin=date2&period=p . date1 is the start date to look for, date2 the finish date to look for and p is the reference timeframe desired by the user. The period variable can be any of the following : h, d, w, m wether the user want an hourly, daily, weekly, or monthly frequentation. We recommand you use the doc available to automatically create your requests.

Third functionality:
 - When looking for the most frequented Paris borough on a period of time, the user would input /fonctionnalite-3/?date_debut=date1&date_fin=date2&period=p . With the same variables as defined above. We recommand you use the doc available to automatically create your requests.

# Installation

The installation is straight forward. First, you have to install the required dependencies, that can be done with the following command :
```
pip install -r requirements.txt
```

Then, all you have to do is to launch the main.py file and connect yourself to the ip provided
