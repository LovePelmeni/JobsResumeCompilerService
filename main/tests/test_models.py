import unittest


class ModelTestCase(unittest.TestCase):

    @parameterized.parameterized([{'username': "Test Username", "email": 'Test_email', 'Password': "TEst Password"}])
    def test_model_create(self,  customer_data):
        models.Customer.objects.create(**customer_data)
        self.assertGreater(len(models.Customer.objects.all()), 0)


    @parameterized.parameterized([{'username': 'Test Username', 'email': "Test Email"}])
    def test_model_update(self, updated_data):
        customer = models.Customer.objects.create()
        old_customer_username = customer.username
        customer.update(**updated_data)
        self.assertNotEqual(customer.username, old_customer_username)


    def test_model_delete(self):
        customer_data = {}
        customer = models.Customer.objects.create(**customer_data)
        customer.delete()
        self.assertLess(len(models.Customer.objects.all()), 2)

