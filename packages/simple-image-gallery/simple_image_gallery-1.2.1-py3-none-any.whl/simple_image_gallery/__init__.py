import logging
import sys

from flask import Flask
from flask_injector import FlaskInjector

from simple_image_gallery.configuration.config import GalleryConfig
from simple_image_gallery.configuration.modules import ServiceModule
from simple_image_gallery.controller import index, images, diashow

Flask.url_for.__annotations__ = {}  # Workaround: https://github.com/python-injector/flask_injector/issues/78

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(GalleryConfig())

    app.register_blueprint(index.index_bp)
    app.register_blueprint(images.images_bp)
    app.register_blueprint(diashow.diashow_bp)

    FlaskInjector(app, modules=[ServiceModule])
    return app
