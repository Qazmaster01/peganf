from django.test import TestCase
import unittest

class TestBank(TestCase):
    def cheak_create_back(self):
        custom_bank = Bank.object.create(
            name = "Test1",
            bic = "123456",
            address = "Astana"
        )
        self.assertIsNotNone(custom_bank)
        self.assertEqual(custom_bank.name, "Test1")
        self.assertEqual(custom_bank.bic, "123456")
        self.assertTrue(custom_bank.activated)

if __name__ == '__main__':
    unittest.main()
