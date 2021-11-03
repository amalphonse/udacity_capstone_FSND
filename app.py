import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth

from models import setup_db, Actors, Movies



PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #Pagination
  def paginate(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page-1) * PER_PAGE
    end = start + PER_PAGE
      
    records = [records.format() for records in selection]
    current_records = records[start:end]
      
    return current_records


  '''
  Using after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/',methods=['GET'])
  def get_init():
    return jsonify({
      'success':True,
      'message': "Casting Agency App. Default page."
    })


  '''
  Implemented GET requests for actors, 
  -GET '/actors' including pagination (every 10 records). 
  -This endpoint returns a list of actors, 
  number of total actors. 

  '''

  @app.route('/actors',methods=['GET'])
  @requires_auth(permission='get:actors')
  def get_actors(payload):
    selection = Actors.query.order_by(Actors.id).all()
    current_selection = paginate(request,selection)
    return jsonify({
      'success':True,
      'actors':current_selection,
      'total_actors':len(Actors.query.all()),
    })

  '''
  Implemented POST requests for actors, 
  - POST /actors
  - This endpoint gets the json using get_json()
  - This endpoint returns the success and the id of the actor added.

  '''

  @app.route('/actors', methods=['POST'])
  @requires_auth(permission='post:actors')
  def create_actors(payload):
    body = request.get_json()

    name = body.get('name',None)
    gender = body.get('gender',None)
    age = body.get('age',None)

    if name is None or gender is None or age is None:
      abort(422)
    
    try:
      new_actor = Actors(name=name,gender=gender,age=age)
      new_actor.insert()
      return jsonify({
        'success':True,
        'actor_added': new_actor.id
      })
    except Exception as e:
      #print('Failed to <insert|delete|update> on <actor|movie>: '+ str(e))
      abort(422)

  '''
  Implemented PATCH requests for actors, 
  - PATCH '/actors'.
  - This endpoint is to update an actor based on id.
  - This endpoint returns id of the updated actor and success.
  '''

  @app.route('/actors/<int:id>',methods=['PATCH'])
  @requires_auth(permission='patch:actors')
  def update_actors(payload,id):
    
    actor = Actors.query.filter(Actors.id==id).one_or_none()

    if actor is None:
      abort(404)
     
    body = request.get_json()
    if body is None:
      abort(422)
    try:     
      if 'name' in body:
        actor.name = body['name']
        
      if 'gender' in body:
        actor.gender = body['gender']
        
      if 'age' in body:
        actor.age = body['age']
      actor.update()
      return jsonify({
          'success':True,
          'actor-updated':id
        })
    except Exception:
      abort(422)
  '''
  Implemented DELETE requests for actors, 
  - DELETE '/actors'.
  - This endpoint is to delete an actor based on id.
  - This endpoint returns id of the deleted actor and success.
  '''

  @app.route('/actors/<int:id>',methods=['DELETE'])
  @requires_auth(permission='delete:actors')
  def delete_actor(payload,id):
    
    actor = Actors.query.filter(Actors.id==id).one_or_none()

    if actor is None:
      abort(404)
    try:  
      actor.delete()

      return jsonify({
        'success': True,
        'deleted-actor': actor.id
      })
    except Exception:
      abort(422)


  '''
  Movies API calls
  '''

  '''
  Implemented GET requests for movies, 
  -GET '/movies' including pagination (every 10 records). 
  -This endpoint returns a list of movies, 
  number of total movies. 
  '''

  @app.route('/movies',methods=['GET'])
  @requires_auth(permission='get:movies')
  def get_movies(payload):
    try:
      selection = Movies.query.order_by(Movies.id).all()
      current_selection = paginate(request,selection)
      return jsonify({
        'success':True,
        'movies':current_selection,
        'total_movies':len(Movies.query.all()),
      })
    except Exception:
      abort(422)

  '''
  Implemented POST requests for movies, 
  - POST /movies
  - This endpoint gets the json using get_json()
  - This endpoint returns the success and the id of the movie added.

  '''

  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='post:movies')
  def create_movies(payload):
    try: 
      body = request.get_json()

      title = body.get('title',None)
      release_date = body.get('release_date',None)

      if title is None or release_date is None:
        abort(422)

      new_movie = Movies(title=title,release_date=release_date)

      new_movie.insert()
      return jsonify({
        'success':True,
        'new-movie-added': new_movie.id
      })
    except Exception as e:
      #print('Failed to <insert|delete|update> on <actor|movie>: '+ str(e))
      abort(422)

  '''
  Implemented PATCH requests for movies, 
  - PATCH '/movies'.
  - This endpoint is to update an movie based on id.
  - This endpoint returns id of the updated movie and success.
  '''

  @app.route('/movies/<int:id>',methods=['PATCH'])
  @requires_auth(permission='patch:movies')
  def update_movie(payload,id):
    try: 
      movie = Movies.query.filter(Movies.id==id).one_or_none()

      if movie is None:
        abort(404)
      
      body = request.get_json()
      if body is None:
        abort(422)
    
      if 'title' in body:
        movie.name = body['title']
      
      if 'gender' in body:
        movie.release_date = body['release_date']
      
      movie.update()

      return jsonify({
        'success':True,
        'movie-updated':movie.id
      })
    except Exception:
      abort(422)

  '''
  Implemented DELETE requests for movies, 
  - DELETE '/movies'.
  - This endpoint is to delete an movie based on id.
  - This endpoint returns id of the deleted movie and success.
  '''

  @app.route('/movies/<int:id>',methods=['DELETE'])
  @requires_auth(permission='delete:movies')
  def delete_movie(payload,id):
    
    movie = Movies.query.filter(Movies.id==id).one_or_none()

    if movie is None:
      abort(404)
    try:  
      movie.delete()

      return jsonify({
        'success': True,
        'deleted-movie': movie.id
      })
    except Exception:
      abort(422)

  '''
    @Error Handlers: 
    Created error handlers for all expected errors 
    including 404 and 422. 
    '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400


  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Permission not found"
        }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "forbidden"
        }), 403

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)