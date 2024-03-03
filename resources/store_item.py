from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from db import db

from resources.schemas import ItemSchema, ItemUpdateSchema

from db import items

blp = Blueprint('Store Items', __name__, description='Operation on store item')

@blp.route('/item')
class StoreItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Error occured while inserting item')

        return item
    
@blp.route('/item/<string:item_id>')
class StoreItem(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError('Updating an item is not implemented')

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError('Updating an item is not implemented')