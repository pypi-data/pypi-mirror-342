from flask import Blueprint, send_from_directory, request, Response, url_for

from simple_image_gallery.services.images import ImageService

images_bp = Blueprint('images', __name__, url_prefix='/images')


@images_bp.get('/<filename>')
def query_image(filename: str, service: ImageService):
    # Returns an image from the gallery directory
    file_path = service.find_image_path(filename)
    return send_from_directory(file_path.parent, filename)


@images_bp.get('/default.png')
def query_default_image():
    # Returns a default image
    return send_from_directory('static', 'img/default.png')


@images_bp.get('')
def query_image_paths(service: ImageService):
    # Get query parameters
    sort = request.args.get('sort', 0, int)
    min_items = request.args.get('min_items', service.gallery_diashow_min_batch_size, int)
    # Get the image paths
    image_paths = service.get_image_paths(sort, min_items=min_items)
    return [url_for('images.query_image', filename=path.name) for path in image_paths]


@images_bp.post('')
def download_images(service: ImageService):
    # Allows downloading a single image or a zip archive of multiple images
    images = list(request.form.keys())
    match len(images):
        case 0:  # No images selected
            return Response('No images selected', status=400)
        case 1:  # Return the image directly
            data, mimetype = service.read_image(images[0])
            filename = images[0]
        case _:  # Create a zip archive
            data, mimetype = service.create_image_archive(images)
            filename = service.image_archive_name
    return Response(data, mimetype=mimetype, headers={'Content-Disposition': f'attachment; filename={filename}'})
