from flask import Config
from injector import Module, provider

from simple_image_gallery.services.images import ImageService


class ServiceModule(Module):

    @provider
    def provide_images_service(self, config: Config) -> ImageService:
        return ImageService(config)