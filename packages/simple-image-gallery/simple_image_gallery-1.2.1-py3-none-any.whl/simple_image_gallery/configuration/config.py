import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GalleryConfig(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    GALLERY_HOST: str = Field(default='127.0.0.1')
    GALLERY_PORT: int = Field(default=8080, gt=0)
    GALLERY_DIRECTORY: str = Field(default_factory=os.getcwd)
    GALLERY_IMAGE_DATE_FORMAT: str = '%m/%d/%Y %I:%M %p'
    GALLERY_HEADER: str = 'my gallery'
    GALLERY_DIASHOW_MIN_BATCH_SIZE: int = Field(default=5, gt=0)
