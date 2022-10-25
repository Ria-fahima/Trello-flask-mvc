from flask import Blueprint,request
from datetime import date
from db import db
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
# @jwt_required()
def get_all_cards():
    # return 'all cards route'
    # if not authorize():
    #     return {'error': 'You must be an admin'},401
    #select * from cards;
    # cards = Card.query.all()
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)
    return CardSchema(many = True).dump(cards)


@cards_bp.route('/<int:id>/')
def get_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': f'card not found with id {id}'}, 404

@cards_bp.route('/<int:id>/', methods=['DELETE'])
def delete_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'message': f'Card {card.title} deleted successfully'}
    else:
        return {'error': f'card not found with id {id}'}, 404


@cards_bp.route('/<int:id>/', methods = ['PUT', 'PATCH'])
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        card.title = request.json.get('title') or card.title
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status
        card.priority = request.json.get('priority') or card.priority
        db.session.commit()
        return CardSchema().dump(card)
    else:
        return {'error': f'card not found with id {id}'}, 404


@cards_bp.route('/',methods=['POST'])
def create_card():
    
    card = Card(
        title = request.json['title'], 
        description = request.json['description'],
        date = date.today(),
        status = request.json['status'],
        priority = request.json['priority']
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201
    