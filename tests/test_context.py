
import re
import unittest

from nanohttp import Controller, text, ContextIsNotInitializedError, context, Context
from tests.helpers import WsgiAppTestCase


class ContextProxyTestCase(unittest.TestCase):

    def test_context(self):
        self.assertRaises(ContextIsNotInitializedError, Context.get_current)


class ContextTestCase(WsgiAppTestCase):

    class Root(Controller):

        @text
        def get_uri(self):
            yield context.request_uri

        @text
        def get_scheme(self):
            yield context.request_scheme

        @text('post')
        def get_request_content_length(self):
            yield str(context.request_content_length)


    def test_redirect_response_header(self):
        self.assert_get(
            '/get_uri',
            query_string={'a': 1, 'b': 2},
            expected_response=re.compile('http://nanohttp.org/get_uri\?[ab=12&]+')
        )

        self.assert_get(
            '/get_scheme',
            expected_response='http'
        )

        self.assert_post(
            '/get_request_content_length',
            fields={
                'a': 1,
                'b': [2, 3],
            },
            expected_response='18'
        )



