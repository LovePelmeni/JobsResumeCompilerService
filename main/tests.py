from django.test import TestCase
import unittest.mock
# Create your tests here.


class ResumeRendererTestCase(unittest.TestCase):

    def mocked_cv_content(self):
        return """<body><h1>Correct Content</h1></body>"""

    def mocked_fake_cv_content(self):
        return """Invalid CV Content File"""

    @unittest.mock.patch('main.tests.ResumeRendererTestCase.mocked_cv_content')
    def test_render_to_pdf(self, mocked_cv_content):
        from . import renderers
        renderer = renderers.CVPDFRenderer()
        pdf_resume = renderer.render(mocked_cv_content, cv_name='Test CV')
        self.assertIsInstance(pdf_resume, typing.Type['TextIO'], msg='Invalid Content Has been Returned.')


    @unittest.mock.patch('main.tests.ResumeRendererTestCase.mocked_fake_cv_content')
    def test_render_to_pdf_fail(self, fake_cv_content):
        from . import renderers
        with self.assertRaises(expected_exception=rest_framework.exceptions.APIException):
            renderer = renderers.CVPDFRenderer()
            renderer.render(fake_cv_content, cv_name='Invalid CV')


class ResumeSuggestionsTestCase(unittest.TestCase):

    def test_get_suggestions(self):
        pass

class CustomerControllerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_customer_create(self):
        pass

    def test_customer_update(self):
        pass

    def test_customer_delete(self):
        pass


class TopicControllersTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_topic_create(self):
        pass

    def test_topic_update(self):
        pass

    def test_topic_delete(self):
        pass


