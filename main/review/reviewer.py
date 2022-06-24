from abc import ABC
from . import exceptions
from . import resume_review_issues


class ResumeParser(abc.ABC):

    def __init__(self, resume: Resume):
        self.resume = resume

    @abc.abstractmethod
    def parse_resume(self) -> typing.Dict[str, typing.Any]:
        """
        // * Parses whole resume basically returns methods
        `parse_topics` and `parse_title` and merge the context.
        """

    @abc.abstractmethod
    def parse_topics(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        // * Parses Resume Topics.
        """
    @abc.abstractmethod
    def parse_title(self) -> str:
        """
        // * Parses Resume Title
        """

class BaseReviewer(abc.ABC):

    def __init__(self, resume):
        self.resume_parser = ResumeParser(resume)
        self.resume = self.resume_parser.parse_resume()

    @abc.abstractmethod
    def review(self):
        """
        // * Reviews the resume, checks for spelling and
        correctness of the resume, checks for length and stuff like that
        `Implements the interface of the reviewer,
        review the resume using Specific AI written in TensorFlow (python).
        """

class ResumeReviewer(BaseReviewer):

    def __init__(self, resume: typing.Dict[str, typing.Any]):
        self.resume = resume
        super(BaseReviewer, self).__init__(resume)

    def review(self):
        import requests
        try:
            response = requests.post('http://%s:8006/validate/resume/',
            data={'resume': self.resume}, timeout=10)
            if 'errors' in json.loads(response.text).keys():
                return response.json()
            return None
        except(requests.exceptions.Timeout):
            raise TimeoutError()
