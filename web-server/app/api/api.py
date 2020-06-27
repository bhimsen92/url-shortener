from flask import Blueprint

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/<url_id>")
def redirect(url_id):
    pass


@api_blueprint.route("/<url_id>/<sub_url>")
def redirect_redirect(url_id, sub_url):
    pass


@api_blueprint.route("/shorten")
def shorten_url():
    pass
