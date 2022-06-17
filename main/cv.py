import pydantic, typing, django.core.exceptions
import typing


class CVContent(pydantic.BaseModel):

    data_content: str

    @staticmethod
    def valid_content(value):
        pass

    @pydantic.validator('data_content')
    def validate_data_content(cls, value) -> typing.Union[str, Exception]:
        if not cls.valid_content(value):
            raise django.core.exceptions.ValidationError(message='Invalid Content')
        return value