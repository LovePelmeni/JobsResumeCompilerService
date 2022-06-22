import rest_framework.exceptions
from rest_framework import renderers
import typing

class RendererError(Exception):

    def __init__(self, reason: str):
        self.reason = reason

class RendererMixin(object):

    accepted_media_types: typing.ClassVar[typing.List[str]] = \
   ('application/json', 'application/xml', 'text/plain', 'application/www-form-urlencoded')

    def __call__(self, *args, **kwargs):
        self.check_content_valid(**kwargs)
        return self.render(**kwargs)

    def render(self, data, cv_name: str, accepted_types=None, renderer_context=None) -> bytes:
        """/ * This method suppose to be overridden"""

    def check_content_valid(self, data, renderer_context, accepted_media_type):
        if not isinstance(data, str):
            raise RendererError(reason='Invalid Type Of Content. Required Str. Got %s' % type(data))
        if not isinstance(renderer_context, dict) or not accepted_media_type in self.accepted_media_types:
            message = 'Accepted Type not allowed or invalid renderer context.'
            raise RendererError(reason=message)


class CVPDFRenderer(RendererMixin, renderers.BaseRenderer):

    accepted_media_types = ()

    def render_to_pdf(self, content: str, cv_name: str) -> typing.Type['TextIO']:
        pass

    def render(self, data, cv_name: str, accepted_media_type=None, renderer_context=None):
        try:
            content = self.render_to_pdf(content=data, cv_name=cv_name)
            return content
        except(rest_framework.exceptions.APIException) as exception:
            logger.error("Renderer Exception: %s" % exception)
            raise rest_framework.exceptions.APIException(
            )

class CVWordRenderer(RendererMixin, renderers.BaseRenderer):

    accepted_media_types = ()

    def render_to_word_document(self, content: str):
        pass

    def render(self, data, cv_name: str, accepted_media_type=None, renderer_context=None):
        try:
            content = self.render_to_word_document(content=data)
            return content
        except(rest_framework.exceptions.APIException) as exception:
            logger.error('Word Renderer Exception: %s' % exception)
            raise rest_framework.exceptions.APIException()


