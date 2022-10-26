from init import db,ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    user = db.relationship("User", back_populates = "cards")
class CardSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['password'])
    class Meta:
        fields = ('id','title','description','status','priority','date', 'user')
        ordered = True