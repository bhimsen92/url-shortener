from flask import Blueprint, request, jsonify, redirect
from werkzeug.exceptions import BadRequest
from snowflake.client import SnowFlakeClient
from models import Urls
from psycopg2.errors import UniqueViolation

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/<url_id>")
def redirect_(url_id):
    try:
        result = Urls.get_original_url(url_id=url_id)
        if result:
            return redirect(result[0]["original_url"])
        raise Exception("url_id: %s not found in db. It is probably expired." % url_id)
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


@api_blueprint.route("/<url_id>/<sub_url>")
def redirect_redirect(url_id, sub_url):
    try:
        result = Urls.get_original_url(url_id=url_id)
        if result:
            url = "%s/%s" % (result[0]["original_url"], sub_url)
            return redirect(url)
        raise Exception("url_id not found in db. It is probably expired." % url_id)
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


@api_blueprint.route("/shorten", methods=["POST"])
def shorten_url():
    payload = {}
    try:
        payload = request.get_json()
        original_url = payload.get("original_url", None)
        if not original_url:
            raise BadRequest("please provide url to shorten: %s" % original_url)
        url_id = payload.get("custom_id", None)
        if not url_id:
            url_id = SnowFlakeClient.get_unique_url_id()
        Urls.store_url(original_url=original_url, url_id=url_id)
        return jsonify({
            "url_id": url_id,
            "new_url": "%s/%s" % ("http://localhost:8000", url_id)
        })
    except BadRequest as e:
        return jsonify({
            "message": e.message
        })
    except UniqueViolation as e:
        message = "No unique ids available at the moment. Please try again later."
        if payload.get("custom_id"):
            message = "custom url id: %s is not available. Please try with some other id." % payload.get("custom_id")
        return jsonify({
            "message": message
        })
    except Exception as e:
        return jsonify({
            "message": "Service seems to be down. Please try again later."
        })
