# Udacity Capstone Full Stack Nano Degree - Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql casting_agency < casting_agency.psql
```

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file to find the application. 


## API Reference

### Getting Started
- The app is hosted on herouku https://casting-agency-anju.herokuapp.com/ 
- Authentication uses Auth0 authentication. The current tokens are with in the test_app.py file.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: unauthorized
- 403: forbidden
- 404: Resource Not Found
- 422: unprocessable

### Endpoints 

#### GET '/actors'
- General:
    - Fetches a list of actors with their id, name, age and gender.
    - Request Arguments: None
    - Returns a list of movies with pagnination in groups of 10 along with number of total movies, success.

    ```
        "actors": [
        {
            "age": "50",
            "gender": "female",
            "id": 1,
            "name": "Daphne"
        },
        {
            "age": "49",
            "gender": "male",
            "id": 2,
            "name": "Fraiser"
        },
        {
            "age": "30",
            "gender": "female",
            "id": 3,
            "name": "Monica"
        },
        {
            "age": "45",
            "gender": "Male",
            "id": 5,
            "name": "Jerry"
        },
        {
            "age": "45",
            "gender": "Male",
            "id": 6,
            "name": "George"
        }
    ],
    "success": true,
    "total_actors": 5
}
    ```

#### GET '/movies'
- General:
    - Returns a list of movies with pagnination in groups of 10 along with number of total movies, success.


```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 03 Nov 2020 00:00:00 GMT",
            "title": "Violet"
        },
        {
            "id": 3,
            "release_date": "Tue, 03 Nov 2020 00:00:00 GMT",
            "title": "Wolf"
        },
        {
            "id": 4,
            "release_date": "Thu, 22 Oct 2020 00:00:00 GMT",
            "title": "Dune"
        },
        {
            "id": 5,
            "release_date": "Thu, 22 Oct 2020 00:00:00 GMT",
            "title": "Antlers"
        }
    ],
    "success": true,
    "total_movies": 4
}
```

#### POST '/actors'
- General:
    - To create a new actor with name, age and gender,
    - Returns the success value and id of the created actors. 

```
{
  "id": 5,
  "success": True
}
```

#### POST '/movies'
- General:
    - To create a new movie with title and release date.
    - Returns the success value and id of the created movie. 

```
{
  "id": 4,
  "success": True
}
```

#### PATCH '/actors/{actor_id}'
- General:
    - Patch the actor of the given ID if it exists. 
    - Returns the id of the updated actor, success value.

```
{
  "success": True,
  "actor-updated": 1
}
```

#### PATCH '/movies/{movie_id}'
- General:
    - Patch the movie of the given ID if it exists. 
    - Returns the id of the updated movie, success value.
```
{
  "success": True,
  "deleted": 2
}
```

#### DELETE '/actors/{actor_id}'
- General:
    - Deletes the actor of the given ID if it exists. 
    - Returns the id of the deleted actor, success value.
```
{
  "success": True,
  "deleted": 2
}
```

#### DELETE '/movies/{movie_id}'
- General:
    - Deletes the movie of the given ID if it exists. 
    - Returns the id of the deleted movie, success value.
```
{
  "success": True,
  "deleted": 1
}
```


## Deployment
Deployed on heroku.

## Authors
Anju Mercian and the Udacity Team.

## Run Database Migrations

Note: Use 'python3 manage.py db init' if you have two versions installed 

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

## Testing

Note: The owner will need to be changed for the postgres sql.
To run the tests, run
```
dropdb casting_agency
createdb casting_agency
psql casting_agency < casting_agency.psql
python test_app.py
```












