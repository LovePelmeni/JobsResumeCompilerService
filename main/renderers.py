import rest_framework.exceptions
from rest_framework import renderers

class RendererError(Exception):

    def __init__(self, reason: str):
        self.reason = reason

class RendererMixin(object):

    accepted_media_types = typing.Classvar[typing.List[str]] = \
   ('application/json', 'application/xml', 'text/plain', 'application/www-form-urlencoded')

    def __call__(self, *args, **kwargs):
        self.check_content_valid()
        return self.render(**kwargs)

    def render(self, data, accepted_types=None, renderer_context=None) -> bytes:
        """/ * This method suppose to be overridden"""

    def check_content_valid(self):
        if not isinstance(renderer_context, dict) or not accepted_media_type in self.accepted_media_types:
            message = 'Accepted Type not allowed or invalid renderer context.'
            raise RendererError(reason=message)


class CVPDFRenderer(RendererMixin, renderers.BaseRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            pass
        except(rest_framework.exceptions.APIException) as exception:
            logger.error("Renderer Exception: %s" % exception)
            raise rest_framework.exceptions.APIException(
            )

class CVWordRenderer(RendererMixin, renderers.BaseRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            pass
        except(rest_framework.exceptions.APIException) as exception:
            logger.error('Word Renderer Exception: %s' % exception)
            raise rest_framework.exceptions.APIException()



