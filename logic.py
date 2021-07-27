from oto import response
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from flask import jsonify
from database import db_session
from model import Cat


def get_cats():

    entities_list = []

    try:
        data = db_session.query(Cat).all()

    except(SQLAlchemyError, DBAPIError):

        return jsonify({
            'status': 'error',
            'message': 'Something went wrong...',
        })

    for entity in data:
        entities_list.append({'id': entity.id, 'name': entity.name, 'breed': entity.breed, 'color': entity.color})


    if len(entities_list) == 0:
        return  response.Response(" DB is empty")

    return response.Response(entities_list)



def get_cat_by_id(cat_id):
    try:
        entity = db_session.query(Cat).filter(Cat.id == cat_id).first()
    except(SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'Something went wrong...',
            'data': []
        })

    if not entity:
        return response.Response("There is no cat with such id")
    cat = {'id': entity.id, 'name': entity.name, 'breed': entity.breed, 'color': entity.color}
    return response.Response(cat)

def create_cat(name, breed, color):

    try:
        new_entity = Cat(name=name, breed=breed, color=color)
        db_session.add(new_entity)
        db_session.commit()
    except (SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'Some kind of error happened while adding to database...'
        })
    cat = {"name": name, "breed":breed, "color":color}
    return response.Response(cat, {
        'message': 'New cat was added to database...',
        "cat": cat,
    })

def remove_cat(cat_id):
    entity = db_session.query(Cat).filter(Cat.id == cat_id).first()
    try:
        entity.delete()
        entity.commit()
    except (SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'error happened while deleting from database...',
        })
    return response.Response( 'Entity was deleted successful...')

