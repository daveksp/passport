from __future__ import absolute_import

import logging

from datetime import datetime
from flask import current_app, request, g, has_request_context
import json

from .utilities import request_ids, redact_sensitive_data


sensitive_fields = ['client_secret', 'token', 'access_token']


def setup_logging(app):
    class ApiFilter(logging.Filter):
        def filter(self, record):
            record.environment = app.config.get('ENVIRONMENT')
            if has_request_context():
                request_id, original_request_id = request_ids()
                record.request_id = request_id
                record.original_request_id = original_request_id
                record.request_url = request.url
                record.request_method = request.method
                record.remote_addr = request.remote_addr
                record.endpoint = request.endpoint
            return True

    app.logger.addFilter(ApiFilter())

    @app.before_request
    def log_request_info():
        g.start = datetime.now()

        request_id, original_request_id = request_ids()
        log_data = {'request-id': str(request_id),
                    'original-request-id': original_request_id,
                    'user-agent': request.headers.get('User-Agent'),
                    'url': request.url}

        data = request.json or {}
        log_data['data'] = redact_sensitive_data(data, sensitive_fields)
        current_app.logger.info('Request Data: {0}'.format(log_data))

    @app.after_request
    def log_response_info(response):
        time = datetime.now() - g.start
        request_id, original_request_id = request_ids()
        log_data = {'url': request.url,
                    'response_code': response.status_code,
                    'time': time.seconds + time.microseconds / 10. ** 6,
                    'request-id': str(request_id),
                    'original-request-id': original_request_id}

        try:
            data = json.loads(response.data)
        except ValueError:
            data = {}

        if not isinstance(data, list):
            data = redact_sensitive_data(data, sensitive_fields)
        log_data['data'] = data

        current_app.logger.info('Response Data: {0}'.format(log_data))
        return response
