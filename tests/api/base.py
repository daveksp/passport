from flask_testing import TestCase

from postal_service import create_app


class IntegrationTestCase(TestCase):

    def create_app(self):
        self.app = create_app(settings_override={})
        self.app.config['TESTING'] = True

        return self.app
