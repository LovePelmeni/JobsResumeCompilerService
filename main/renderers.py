import rest_framework.exceptions
from rest_framework import renderers

class RendererError(Exception):

    def __init__(self, reason: str):
        self.reason = reason


class CVPDFRenderer(renderers.BaseRenderer):

    accepted_media_types = ('application/json', 'application/xml', 'text/plain', 'application/www-form-urlencoded')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not isinstance(renderer_context, dict) or not accepted_media_type in self.accepted_media_types:
            message = 'Accepted Type not allowed or invalid renderer context.'
            raise RendererError(reason=message)
        try:
            pass
        except(rest_framework.exceptions.APIException) as exception:
            logger.error("Renderer Exception: %s" % exception)
            raise rest_framework.exceptions.APIException(
            )

class CVRenderer(renderers.BaseRenderer):

    accepted_media_types = ('application/json', 'application/xml', 'text/plain', 'application/www-form-urlencoded')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        pass




