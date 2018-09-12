from flask import Blueprint

item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/item/<string:name>')
def item_page():
    pass


@item_blueprint.route('/load')
def load_item():
    """
    Loads an item data using their store and return a json representation of it
    :return:
    """
    pass
