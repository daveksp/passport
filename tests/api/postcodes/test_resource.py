import json
from mock import patch
from nose.tools import eq_

from ..base import IntegrationTestCase
from postal_service.api import postcodes
from postal_service.api.exceptions import (PostcodeNotValidException,
                                           RequestDataException)
from postal_service.api.common.failures import Failures as CommonFailures
from postal_service.api.postcodes.failures import Failures


@patch('postal_service.api.postcodes.request')
class PostcodesTests(IntegrationTestCase):

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def setUp(self):
        self.resource = postcodes.PostcodeResource()

    def test_get(self, mock_request):
        mock_request.args = {'postcode': 'FY2 2AD'}
        response = self.resource.get()
        eq_(json.loads(response.data)['is_valid'], True)

    def test_get_missing_postcode(self, mock_request):
        mock_request.args = {}
        with self.assertRaises(RequestDataException) as context:
            self.resource.get()
        eq_(context.exception.errors, CommonFailures.information_missing)

    def test_get_invalid_format(self, mock_request):
        mock_request.args = {'postcode': 'FF 2AD'}
        with self.assertRaises(PostcodeNotValidException) as context:
            self.resource.get()
        eq_(context.exception.errors, Failures.invalid_information)

    def test_post(self, mock_request):
        mock_request.json = {
            'area': 'FY', 'district': '2', 'sector': '2', 'unit': 'DF'}
        response = self.resource.post()
        eq_(json.loads(response.data)['is_valid'], True)

    def test_post_invalid_format(self, mock_request):
        mock_request.json = {
            'area': 'FY', 'district': 'C', 'sector': '2', 'unit': 'DF'}
        with self.assertRaises(PostcodeNotValidException) as context:
            self.resource.post()
        eq_(context.exception.errors, Failures.invalid_information)

    def test_post_missing_information(self, mock_request):
        mock_request.json = {
            'area': 'FY', 'sector': '2', 'unit': 'DF'}
        with self.assertRaises(RequestDataException) as context:
            self.resource.post()
        failure = CommonFailures.information_missing
        failure['details'] = {
            'district': [u'Missing data for required field.']}
        eq_(context.exception.errors, failure)
