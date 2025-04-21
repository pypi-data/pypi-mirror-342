from flask import Flask
from waitress import serve

from simple_image_gallery import create_app


def serve_app(app: Flask):
    """Serve the Flask application using Waitress."""
    host, port = app.config['GALLERY_HOST'], app.config['GALLERY_PORT']
    serve(app, host=host, port=port)


def main():
    app = create_app()
    serve_app(app)


if __name__ == "__main__":
    main()
