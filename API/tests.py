import unittest.mock



class ReviewerTestCase(unittest.TestCase):

    def mocked_context(self):
        pass

    def mocked_fake_context(self):
        return """Invalid Context"""

    @unittest.mock.patch('')
    def test_reviewer(self):
        pass

    def test_fail_reviewer(self):
        pass