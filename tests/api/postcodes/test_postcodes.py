from nose.tools import eq_
from unittest import TestCase

from postal_service.api.exceptions import PostcodeNotValidException
from postal_service.api.postcodes.failures import Failures
from postal_service.api.postcodes.models import Postcode


class PostcodesTests(TestCase):

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def test_regular_constructor(self):
        postcode = Postcode('BR', '1', '2', 'AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_iter(self):
        attrs = ['BR', '1', '2', 'AB']
        postcode = Postcode(*attrs)
        for i, attr in enumerate(postcode):
            eq_(attr, attrs[i])

    def test_format(self):
        postcode = Postcode('BR', '1', '2', 'AB')
        eq_(format(postcode), 'BR1 2AB')

    def test_eq(self):
        postcode = Postcode('BR', '1', '2', 'AB')
        other_postcode = Postcode('BR', '1', '2', 'AB')
        eq_(True, postcode == other_postcode)

    def test_str_and_repr(self):
        postcode = Postcode('BR', '1', '2', 'AB')
        eq_(str(postcode), "('BR', '1', '2', 'AB')")
        eq_(postcode, eval(repr(postcode)))

    def test_from_string(self):
        postcode = Postcode.from_string('BR1 2AB')
        eq_(isinstance(postcode, Postcode), True)
        eq_(postcode.area, 'BR')
        eq_(postcode.district, '1')
        eq_(postcode.sector, '2')
        eq_(postcode.unit, 'AB')

    def test_from_string_AA9A(self):
        postcode = Postcode.from_string('BR2A 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_A9A(self):
        postcode = Postcode.from_string('B2A 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_A9(self):
        postcode = Postcode.from_string('B2 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_A99(self):
        postcode = Postcode.from_string('B22 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_AA9(self):
        postcode = Postcode.from_string('BR1 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_AA99(self):
        postcode = Postcode.from_string('BR21 2AB')
        eq_(isinstance(postcode, Postcode), True)

    def test_from_string_invalid_code_format(self):
        with self.assertRaises(PostcodeNotValidException) as context:
            Postcode.from_string('BR1 2B')
        eq_(context.exception.errors, Failures.invalid_information)

    def test_from_string_valid_first_letter(self):
        invalid_letters = ['Q', 'V', 'X']
        valid_letters = set(self.alphabet) - set(invalid_letters)
        for x in valid_letters:
            postcode = Postcode.from_string('{}C2 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_from_string_invalid_first_letter(self):
        invalid_letters = ['Q', 'V', 'X']
        for x in invalid_letters:
            with self.assertRaises(PostcodeNotValidException) as context:
                Postcode.from_string('{}C2 2AB'.format(x))
            eq_(context.exception.errors, Failures.invalid_information)

    def test_from_string_valid_second_letter(self):
        invalid_letters = ['I', 'J', 'Z']
        valid_letters = set(self.alphabet) - set(invalid_letters)
        for x in valid_letters:
            postcode = Postcode.from_string('B{}2 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_from_string_invalid_second_letter(self):
        invalid_letters = ['I', 'J', 'Z']
        for x in invalid_letters:
            with self.assertRaises(PostcodeNotValidException) as context:
                Postcode.from_string('B{}2 2AB'.format(x))
            eq_(context.exception.errors, Failures.invalid_information)

    def test_from_string_valid_third_letter(self):
        valid_letters = 'ABCDEFGHJKPSTUW'
        for x in valid_letters:
            postcode = Postcode.from_string('B2{} 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_from_string_invalid_third_letter(self):
        valid_letters = 'ABCDEFGHJKPSTUW'
        invalid_letters = set(self.alphabet) - set(valid_letters)
        for x in invalid_letters:
            with self.assertRaises(PostcodeNotValidException) as context:
                Postcode.from_string('B2{} 2AB'.format(x))
            eq_(context.exception.errors, Failures.invalid_information)

    def test_from_string_valid_fourth_letter(self):
        valid_letters = 'ABEHMNPRVWXY'
        for x in valid_letters:
            postcode = Postcode.from_string('BB2{} 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_from_string_invalid_fourth_letter(self):
        valid_letters = 'ABEHMNPRVWXY'
        invalid_letters = set(self.alphabet) - set(valid_letters)
        for x in invalid_letters:
            with self.assertRaises(PostcodeNotValidException) as context:
                Postcode.from_string('BB2{} 2AB'.format(x))
            eq_(context.exception.errors, Failures.invalid_information)

    def test_bool_valid_single_digits_districts(self):
        only_single_digit_districts = [
            'BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE',
            'LD', 'SM', 'SR', 'WC', 'WN', 'ZE']
        for x in only_single_digit_districts:
            postcode = Postcode.from_string('{}2 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_bool_invalid_single_digits_districts(self):
        only_single_digit_districts = [
            'BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE', 'LD',
            'SM', 'SR', 'WC', 'WN', 'ZE']
        for x in only_single_digit_districts:
            failure = Failures.invalid_district
            postcode = Postcode.from_string('{}22 2AB'.format(x))
            failure['details'] = (
                "the area {} only have single digit districts".format(x))
            with self.assertRaises(PostcodeNotValidException) as context:
                bool(postcode)
            eq_(context.exception.errors, failure)

    def test_bool_valid_double_digits_districts(self):
        only_double_digit_districts = ['AB', 'LL', 'SO']
        for x in only_double_digit_districts:
            postcode = Postcode.from_string('{}22 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_bool_invalid_double_digits_districts(self):
        only_double_digit_districts = ['AB', 'LL', 'SO']
        for x in only_double_digit_districts:
            failure = Failures.invalid_district
            postcode = Postcode.from_string('{}2 2AB'.format(x))
            failure['details'] = (
                "the area {} only have double digit districts".format(x))
            with self.assertRaises(PostcodeNotValidException) as context:
                bool(postcode)
            eq_(context.exception.errors, failure)

    def test_bool_valid_zero_districts(self):
        zero_digit_districts = [
            'BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']
        for x in zero_digit_districts:
            postcode = Postcode.from_string('{}0 2AB'.format(x))
            eq_(bool(postcode), True)

    def test_bool_invalid_zero_digits_districts(self):
        non_zero_districts = [
            'BR', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE', 'LD',
            'SM', 'SR', 'WC', 'WN', 'ZE', 'AB', 'LL', 'SO']
        for x in non_zero_districts:
            failure = Failures.invalid_district
            postcode = Postcode.from_string('{}0 2AB'.format(x))
            failure['details'] = (
                "the {} area can't have a '0' district".format(x))
            with self.assertRaises(PostcodeNotValidException) as context:
                bool(postcode)
            eq_(context.exception.errors, failure)
