from flask import Flask

from app.webhook.routes import webhook
from .extensions import mongo


# Creating our flask app
def create_app():
    app = Flask(__name__)
    app.config[
        "MONGO_URI"] = "mongodb+srv://demo:demo@cluster0.7vkzs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    mongo.init_app(app)
    # registering all the blueprints

    app.register_blueprint(webhook)

    return app
