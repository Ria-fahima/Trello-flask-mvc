from flask import Blueprint
from db import db
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
# @jwt_required()
def all_cards():
    # return 'all cards route'
    # if not authorize():
    #     return {'error': 'You must be an admin'},401
    #select * from cards;
    # cards = Card.query.all()
    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many = True).dump(cards)


@cards_bp.route('/<int:id>/')
def one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    return CardSchema().dump(card)
