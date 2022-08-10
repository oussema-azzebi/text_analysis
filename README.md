# text_analysis

The API must allow the user to enter a text as input to obtain as output a list of people with some basic information (type, label, description, image, age, country of nationality, etc.).


## 1/ Install and start the app

- Clone the repo:

		git clone https://github.com/oussema-azzebi/text_analysis.git

- Go inside the repo :

		cd text_analysis/

- Create and activate virtual env:

		python3 -m venv env

		source env/bin/activate

- Go inside app:

		cd /app

- Upgrade Pip (Not necessary if you have a recent version of pip)

	        pip3 install --upgrade pip 

- Install dependencies:

		pip3 install -r requirements.txt

- makemigrations and migrate (to generate models) 

		python3 manage.py makemigrations
		python3 manage.py migrate

- Run the server:

		python3 manage.py runserver 


## 2/ example of using the API:

We start with this text : "Hello im Charles Aznavour from France and my friend's name is Michael Caine Emmanuel Kant Jude Law"


- Exemple API person_infos: 

  (POST)  http://127.0.0.1:8000/api/person_infos/Hello im Charles Aznavour from France and my friend's name is Michael Caine Emmanuel Kant Jude Law

The API should return :

[
    {
        "name": "Michael Caine",
        "occupation": "film actor",
        "gender": "male",
        "birthday": "1933-03-14T00:00:00Z",
        "sex": "male",
        "nationality": "United Kingdom",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/Sir%20Michael%20Caine%2C%2028th%20EFA%20Awards%202015%2C%20Berlin%20%28cropped%29.jpg"
    },
    {
        "name": "Jude Law",
        "occupation": "television director",
        "gender": "male",
        "birthday": "1972-12-29T00:00:00Z",
        "sex": "male",
        "nationality": "United Kingdom",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/Jude%20Law%20at%20TIFF2.jpg"
    },
    {
        "name": "Charles Aznavour",
        "occupation": "screenwriter",
        "gender": "male",
        "birthday": "1924-05-22T00:00:00Z",
        "sex": "male",
        "nationality": "France",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/2014.06.23.%20Charles%20Aznavour%20Fot%20Mariusz%20Kubik%2001.jpg"
    }
]


--> This result should be saved in the database 

- Exemple API all_person_listing: 

(GET) /api/all_person_listing

The API should return :

[
    {
        "id": 1,
        "name": "Michael Caine",
        "occupation": "film actor",
        "gender": "male",
        "birthday": "1933-03-14T00:00:00Z",
        "sex": "male",
        "nationality": "United Kingdom",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/Sir%20Michael%20Caine%2C%2028th%20EFA%20Awards%202015%2C%20Berlin%20%28cropped%29.jpg"
    },
    {
        "id": 2,
        "name": "Jude Law",
        "occupation": "television director",
        "gender": "male",
        "birthday": "1972-12-29T00:00:00Z",
        "sex": "male",
        "nationality": "United Kingdom",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/Jude%20Law%20at%20TIFF2.jpg"
    },
    {
        "id": 3,
        "name": "Charles Aznavour",
        "occupation": "screenwriter",
        "gender": "male",
        "birthday": "1924-05-22T00:00:00Z",
        "sex": "male",
        "nationality": "France",
        "image_link": "http://commons.wikimedia.org/wiki/Special:FilePath/2014.06.23.%20Charles%20Aznavour%20Fot%20Mariusz%20Kubik%2001.jpg"
    }
]

- Exemple API all_frequency_listing: 

(GET) /api/all_frequency_listing

The API should return :

[
    {
        "id": 1,
        "person": 1,
        "freq": 1
    },
    {
        "id": 2,
        "person": 2,
        "freq": 1
    },
    {
        "id": 3,
        "person": 3,
        "freq": 1
    }
]

- Exemple API /api/stat_popular_names: 

First we will POST a second Text with a new Charles Aznavour :

http://127.0.0.1:8000/api/person_infos/this is my second text and im also Charles Aznavour


Now we call the API stat_popular_names and it should return :

[
    {
        "name": "Charles Aznavour",
        "appearance frequency": 2
    },
    {
        "name": "Michael Caine",
        "appearance frequency": 1
    },
    {
        "name": "Jude Law",
        "appearance frequency": 1
    }
]


## 3/ To launch units tests  

- Python3 manage.py test





