from nose.tools import eq_
from unittest import TestCase

from passport.api.common.failures import Failure, Failures


class CommonTests(TestCase):
    
    def test_failure_object(self):
        test_failure = Failure({
            "error_category": "test_category",
            "error_type": "test",
            "message": "Testing the Failure Object.",
            "details": None
        })
        eq_(isinstance(test_failure, Failure), True)

    def test_failure_set_details(self):
        Failures.test_failure = Failure({
            "error_category": "test_category",
            "error_type": "test",
            "message": "Testing the Failure Object.",
            "details": None
        })
        editable_failure = Failures.test_failure
        editable_failure['details'] = 'error detail'
        eq_(editable_failure['details'], 'error detail')
        eq_(Failures.test_failure['details'], None)