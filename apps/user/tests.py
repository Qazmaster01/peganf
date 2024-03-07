from django.test import TestCase
from apps.user.models import CustomUser

class CustomUserModelTestCase(TestCase):
    def test_create_custom_user(self):

        custom_user = CustomUser.objects.create(
            phone = '431234536',
            role = 'Client',
            activated = True
        )

        self.assertIsNotNone(custom_user)

        self.assertEqual(custom_user.phone, '431234536')
        self.assertEqual(custom_user.role, 'Client')
        self.assertTrue(custom_user.activated)

if __name__ == '__main__':
    unittest.main()
