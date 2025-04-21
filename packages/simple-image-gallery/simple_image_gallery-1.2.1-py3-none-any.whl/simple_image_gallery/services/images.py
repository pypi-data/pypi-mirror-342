import mimetypes
import random
from glob import glob
from io import BytesIO
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Config

from simple_image_gallery.services.base import BaseService


class ImageService(BaseService):

    def __init__(self, config: Config):
        super().__init__(config)
        self._file_extensions = ['jpg', 'jpeg', 'png']

    def get_image_paths(self, sort: int, min_items: int = None) -> list[Path]:
        """
        Gets a list of paths to images in the gallery directory, sorted by the sort parameter.

        Args:
            sort: 1 for ascending, -1 for descending, 0 for random
            min_items: minimum number of items to return (repeats the list if necessary)
        Returns:
            list: sorted list of image paths
        """
        default_path = Path(__file__).parents[1] / 'static' / 'img' / 'default.png'
        image_paths = self._find_image_paths(default=default_path)
        image_paths_sorted = self._sort_images(image_paths, sort)
        return self._fit_to_min_items(image_paths_sorted, min_items)

    def create_image_archive(self, filenames: list[str]) -> (bytes, str):
        """ Creates an in-memory archive of images specified by their filenames.

        Args:
            filenames: list of image filenames
        Returns:
            tuple: zip archive bytes and mime type
        """
        buffer = BytesIO()
        with ZipFile(buffer, 'w', compression=ZIP_DEFLATED) as archive:
            for name in filenames:
                file_path = self.find_image_path(name)
                archive.write(file_path, name)
        return buffer.getvalue(), 'application/zip'

    def read_image(self, filename: str) -> (bytes, str):
        """ Reads the image from the file system and returns it.

        Args:
            filename: image filename
        Returns:
            tuple: image bytes and mime type
        """
        file_path = self.find_image_path(filename)
        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, 'rb') as img:
            return img.read(), mime_type

    @staticmethod
    def paginate_image_paths(image_paths: list[Path], page: int, items: int) -> list[Path]:
        """
        Paginates a given list of image paths.

        Args:
            image_paths: list of image paths
            page: current page number
            items: number of items per page
        Returns:
            list: paginated list of image paths
        """
        start = (page - 1) * items
        end = start + items
        return image_paths[start:end]

    def _find_images(self) -> Iterable[Path]:
        for g in glob(str(self.gallery_directory)):
            gallery_dir = Path(g)
            for ext in self._file_extensions:
                for img_path in gallery_dir.glob(f'*.{ext}'):
                    yield img_path

    def _find_image_paths(self, default: Path = None) -> list[Path]:
        paths = []
        for image in self._find_images():
            paths.append(image)
        if not paths and default:
            paths.append(default)
        return paths

    def find_image_path(self, filename: str) -> Path | None:
        for image in self._find_images():
            if image.name == filename:
                return image

    @staticmethod
    def _fit_to_min_items(image_paths: [Path], min_items: int | None) -> list[Path]:
        if min_items and len(image_paths) < min_items:
            image_paths *= (min_items // len(image_paths) + 1)
            image_paths = image_paths[:min_items]
        return image_paths

    @staticmethod
    def _sort_images(image_paths: list[Path], sort: int) -> [Path]:
        lst = image_paths.copy()
        match sort:
            case 1:  # Ascending
                lst.sort(key=lambda path: path.stat().st_ctime)
            case -1:  # Descending
                lst.sort(key=lambda path: path.stat().st_ctime, reverse=True)
            case _:  # Random
                random.shuffle(lst)
        return lst

    @property
    def image_archive_name(self) -> str:
        return f'{self.gallery_header}.zip'
