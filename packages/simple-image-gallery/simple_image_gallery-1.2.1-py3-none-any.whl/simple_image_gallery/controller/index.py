from flask import Blueprint, render_template, request

from simple_image_gallery.services.images import ImageService
from simple_image_gallery.utils import time

index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index(service: ImageService):
    # Get query parameters
    sort = request.args.get('sort', -1, int)
    items = request.args.get('items', 20, int)
    page = request.args.get('page', 1, int)
    # Get the image paths and paginate them
    image_paths = service.get_image_paths(sort, min_items=1)
    paginated_paths = service.paginate_image_paths(image_paths, page, items)
    formatted_ctime = [time.format_ctime(path, service.gallery_image_date_format) for path in paginated_paths]
    # Render the template
    template_vars = {
        'images': [(path, formatted_ctime[i]) for i, path in enumerate(paginated_paths)],
        'header': service.gallery_header,
        'sort': sort,
        'items': items,
        'page': page,
        'total_pages': len(image_paths) // items + (len(image_paths) % items > 0)
    }
    return render_template('index.html', **template_vars)
