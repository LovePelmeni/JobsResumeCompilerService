from django.test import TestCase
import unittest.mock
# Create your tests here.


class ResumeRendererTestCase(unittest.TestCase):


    def mocked_cv_content(self):
        return """"""

    def mocked_fake_cv_content(self):
        pass

    @unittest.mock.patch('main.tests.ResumeRendererTestCase.mocked_cv_content')
    def test_render_to_pdf(self, mocked_cv_content):
        pass

    @unittest.mock.patch('main.tests.ResumeRendererTestCase.mocked_fake_cv_content')
    def test_render_to_pdf_fail(self, fake_cv_content):
        pass



class CustomerTestCase(unittest.TestCase):
    pass