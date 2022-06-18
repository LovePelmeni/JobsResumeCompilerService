import lxml.html.html5parser
import pydantic, typing, django.core.exceptions
import typing

class CVContent(pydantic.BaseModel):

    data_content: str

    @staticmethod
    def valid_content(value) -> bool:
        try:
            from lxml import etree
            from io import StringIO
            lxml.etree.parse(StringIO(value),
            parser=lxml.html.html5parser.HTMLParser(recover=False))
            logger.debug('Content has been validated..')
            return True
        except(lxml.etree.ParseError, lxml.etree.ParserError):
            return False

    @pydantic.validator('data_content')
    def validate_data_content(cls, value) -> typing.Union[str, Exception]:
        if not cls.valid_content(value):
            raise django.core.exceptions.ValidationError(message='Invalid Content')
        return value