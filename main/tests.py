from django.test import TestCase
import unittest.mock
# Create your tests here.



class TestModels(unittest.TestCase):


    def test_create(self, model, params):
        model.objects.create(**params)
        assert len(model.objects.all()) > 0

    def test_update(self, model, params):
        obj = model
        new_obj = model.objects.update(**params)
        assert obj.__dict__.items() != new_obj.__dict__.items()

    def test_delete(self, model, obj):
        initial_query = len(model.objects.all())
        assert isinstance(obj, model.__class__)
        obj.delete()
        assert len(model.objects.all()) != initial_query


def resumeSetUp():
    pass

def customerSetUp():
    pass

def topicSetUp():
    pass


unittest.FunctionTestCase(testFunc=TestModels.test_create, setUp=resumeSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_update, setUp=resumeSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_delete, setUp=resumeSetUp)

unittest.FunctionTestCase(testFunc=TestModels.test_create, setUp=customerSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_update, setUp=customerSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_delete, setUp=customerSetUp)

unittest.FunctionTestCase(testFunc=TestModels.test_create, setUp=topicSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_update, setUp=topicSetUp)
unittest.FunctionTestCase(testFunc=TestModels.test_delete, setUp=topicSetUp)

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

class InvalidFormsetPayload(Exception):
    pass

class TestFormsetSubmitResumeCase(unittest.TestCase):

    def mocked_formset_data(self):
        return {}

    @unittest.mock.patch('main.tests.TestFormsetSubmitResumeCase.test_formset_data', autospec=True)
    def test_formset_data(self, mocked_event_data):
        pass