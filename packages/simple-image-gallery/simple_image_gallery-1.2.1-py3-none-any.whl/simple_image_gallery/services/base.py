from flask import Config


class BaseService:

    def __init__(self, config: Config):
        self._config = config

    @property
    def gallery_directory(self) -> str:
        return self._config.get('GALLERY_DIRECTORY')

    @property
    def gallery_header(self) -> str:
        return self._config.get('GALLERY_HEADER')

    @property
    def gallery_image_date_format(self) -> str:
        return self._config.get('GALLERY_IMAGE_DATE_FORMAT')

    @property
    def gallery_diashow_min_batch_size(self) -> int:
        return self._config.get('GALLERY_DIASHOW_MIN_BATCH_SIZE')
