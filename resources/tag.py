from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from resources.schemas import TagSchema, TagAndItemSchema

blp = Blueprint('Tags', __name__, description='Operations on tags')


@blp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        if item.store.id != tag.store.id:
            abort(400, message='make sure that item and tag belongs to the same store')

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, 'an error encountered while inserting the tag')

        return tag
    
    @blp.response(204, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='an error encountered while inserting the tag')

        return dict(message='item removed from tag', item=item, tag=tag)

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202, 
        description='delete a tag if no item is associated with it',
        example={'message': 'tag deleted'}
    )
    @blp.alt_response(404, description='tag not found')
    @blp.alt_response(400, description='returned if the tag is assigned to one or more item. In this case, tag is not deleted')
    def delete(self, tag_id):
        tag = TagModel.query.get(tag_id)

        if not tag:
            abort(404, message='tag not found')

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {}, 204
        
        abort(400, message='could not delete tag, tag is associated with items')

@blp.route('/store/<string:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
            abort(400, message='a tag with that name already exists in that store')

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag