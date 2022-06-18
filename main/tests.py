from django.test import TestCase
import unittest.mock
# Create your tests here.


class ResumeRendererTestCase(unittest.TestCase):

    def mocked_cv_content(self):
        return """<></><></>"""

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
    pass



