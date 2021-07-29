import flask
from flask import Blueprint, request, render_template
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers["Content-Type"] == "application/json":
        response = request.json
        db_obj = mongo.db.events
        if "pusher" in response:
            db_obj.insert_one(
                {'request_id': response["commits"][0]["id"], 'author': response["commits"][0]["author"]["name"],
                 'action': "PUSH",
                 "from_branch": response["repository"]["default_branch"],
                 "to_branch": response["repository"]["default_branch"],
                 "timestamp": response["commits"][0]["timestamp"]})
        elif "pull_request" in response:
            db_obj.insert_one(
                {'request_id': response["sender"]["id"],
                 'author': response["pull_request"]["head"]["repo"]["owner"]["login"],
                 'action': "PULL_REQUEST",
                 "from_branch": response["pull_request"]["head"]["ref"],
                 "to_branch": response["pull_request"]["base"]["ref"],
                 "timestamp": response["pull_request"]["updated_at"]})
    return flask.jsonify(message="success")


@webhook.route("/", methods=["GET"])
def run():
    db_obj = mongo.db.events
    cur = db_obj.find()
    cur_extract = list(cur)
    latest_data = sorted(cur_extract, key=lambda i: i["_id"])
    latest_doc = latest_data[-1]
    return render_template('home.html', data=latest_doc)
