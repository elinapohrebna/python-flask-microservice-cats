import functools
from flask import request, Flask, jsonify
from oto.adaptors.flask import flaskify
import logic
import config

app = Flask(__name__)





def validate_cat_token(function):
    @functools.wraps(function )
    def wrapper( **kwarg):
        cat = request.headers.get('CAT_TOKEN')
        if config.CAT_TOKEN == request.headers.get('CAT_TOKEN'):
            return function(**kwarg)

        return jsonify({
            "status": "error",
            "message": "Invalid token...",
            "cat": cat,
            "tok": config.CAT_TOKEN
        }), 401
    return wrapper

@app.route('/')
def index():
    return jsonify('API IS CURRENTY ONLINE')

@app.route('/cats', methods=['GET'])
@validate_cat_token
def all_cats():
    return flaskify(logic.get_cats())

@app.route('/cat/<cat_id>', methods=['GET'])
@validate_cat_token
def single_cat_by_id(cat_id):
    return flaskify(logic.get_cat_by_id(cat_id))


@app.route('/cat', methods=['POST'])
@validate_cat_token
def create_cat_entity():
    data = request.get_json()
    name = data.get('name')
    breed = data.get('breed')
    color = data.get('color')

    return flaskify(logic.create_cat(name, breed, color) )

@app.route('/cat/{cat_id}', methods=['DELETE'])  # TODO: NEED TO BE FIXED(BACKLOG)
@validate_cat_token
def remove_cat_entity(cat_id):
    return flaskify(logic.remove_cat(cat_id))


if __name__ == '__main__':
    app.run(debug=True)
