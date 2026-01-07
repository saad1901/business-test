from django.test import TestCase
from app.templatetags import phone_extras


class PhoneExtrasTests(TestCase):
    def test_wa_number_10_digits(self):
        self.assertEqual(phone_extras.wa_number('9876543210'), '919876543210')

    def test_wa_number_with_plus(self):
        self.assertEqual(phone_extras.wa_number('+919876543210'), '919876543210')

    def test_wa_number_with_leading_zero(self):
        self.assertEqual(phone_extras.wa_number('09876543210'), '919876543210')

    def test_wa_number_with_spaces_and_symbols(self):
        self.assertEqual(phone_extras.wa_number('+91 98765-43210'), '919876543210')

    def test_wa_number_empty(self):
        self.assertEqual(phone_extras.wa_number(''), '')
