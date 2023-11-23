# ProjetInfo2A
Projet Informatique 2A ENSAI (Sujet 8 : Velib' Hunter)

# Purpose
This application is meant to offer several functionalities to their users in order to manage their access to the Velib' system database.

- For a regular user, he can find the nearest station with available bikes with functionnalite-1 by entering his position - a position that could be written as a usual address instead of geographic coordinates thanks to the use of Etalab API ;
- For a statistical purpose, the Velib' system managers could get access to the least-frequented station on a specific period of time he enters in functionnalite-2 ;
- They could also get access the least-frequented Paris borough on a specific period of time he enters in functionnalite-3. 

# Example

## First functionality:
When searching for the nearest station with at least 1 available bike, the user would input /fonctionnalite-1/ the API will return by default the nearest station to these coordinates 48.8563199, 2.31345367 . But if the user choose to add an input, he can do so in two manners. He can input /fonctionnalite-1/?user_location=lat,lon with lat being the user's latitude and lon the user's longitude. Or he can input /fonctionnalite-1/?user_adress=some_adress with some_adress a plain text adress of the user's location. We recommand using the doc available to automatically create the request for the adress as it is in a special format for the request.

```
http://127.0.0.1:8000/fonctionnalite-1/
```
Will result in :
```
{"station_uuid":7015,"station_name":"Varenne","loc":{"lat":48.857202661803,"lon":2.3152771219611},"numbikes":3,"station_arr":7}
```

```
http://127.0.0.1:8000/fonctionnalite-1/?user_location=48%2C2
http://127.0.0.1:8000/fonctionnalite-1/?user_location=48,2
```
Will both result in :
```
{"station_uuid":21402,"station_name":"Place Aimé Césaire","loc":{"lat":48.783194713067815,"lon":2.2429127991199493},"numbikes":3,"station_arr":null}
```
```
http://127.0.0.1:8000/fonctionnalite-1/?user_adress=14%20Rue%20Dombasle
```
Will result in :
```
{"station_uuid":15052,"station_name":"Convention - Vaugirard","loc":{"lat":48.83767682233156,"lon":2.295586926020252},"numbikes":36,"station_arr":15}
```

## Second functionality:
When looking for the least frequented station on a period of time, the user would input /fonctionnalite-2/?date_debut=date1&date_fin=date2 . date1 is the start date to look for, date2 the finish date to look for. If the user doesn't specify one of those, date1 will be considered as 1-01-01 00:00:00 and date2 as the current date. We recommand you use the doc available to automatically create your requests as the date are in a special format for the request.

```
http://127.0.0.1:8000/fonctionnalite-2/
```
Will result in :
```
{"station_uuid":1001,"station_name":"Quai de l'Horloge - Pont Neuf","loc":{"lat":48.857058739111,"lon":2.3417982839439},"numbikes":2,"station_arr":1}
```

```
http://127.0.0.1:8000/fonctionnalite-2/?date_debut=2023-11-01T00%3A00%3A00
```
Will result in :
```
{"station_uuid":1001,"station_name":"Quai de l'Horloge - Pont Neuf","loc":{"lat":48.857058739111,"lon":2.3417982839439},"numbikes":2,"station_arr":1}
```

```
http://127.0.0.1:8000/fonctionnalite-2/?date_fin=2023-11-23T14%3A30%3A00
```
Will result in :
```
{"station_uuid":1001,"station_name":"Quai de l'Horloge - Pont Neuf","loc":{"lat":48.857058739111,"lon":2.3417982839439},"numbikes":2,"station_arr":1}
```

```
http://127.0.0.1:8000/fonctionnalite-2/?date_debut=2023-11-23T23%3A41%3A00&date_fin=2023-11-23T23%3A56%3A00
```
Will result in :
```
{"station_uuid":1001,"station_name":"Quai de l'Horloge - Pont Neuf","loc":{"lat":48.857058739111,"lon":2.3417982839439},"numbikes":2,"station_arr":1}
```

## Third functionality:
When looking for the most frequented Paris borough on a period of time, the user would input /fonctionnalite-3/?date_debut=date1&date_fin=date2 . With the same variables as defined above. We recommand you use the doc available to automatically create your requests for the same reason explained above.

The usage of the third functionality will be exactly as it is for fhe second functionality except that the user will have to change fonctionnalite-2 into fonctionnalite-3 in the request and the output will be an integer representing the Paris borough

# Installation

The installation is straight forward. First, you have to install the required dependencies, that can be done with the following command :
```
pip install -r requirements.txt
```

Then, all you have to do is to launch the main.py file and connect yourself to the ip provided
