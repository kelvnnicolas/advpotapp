import logging
from django.test import SimpleTestCase


class RequestLogTests(SimpleTestCase):
    def test_access_log_removes_search_content_but_keeps_route_and_status(self):
        from config.logging import RequestPathFilter
        event = logging.LogRecord('django.server', logging.INFO, '', 0, '"%s" %s %s', ('GET /casos/?q=conteudo-reservado HTTP/1.1', '200', '1234'), None)
        self.assertTrue(RequestPathFilter().filter(event))
        self.assertEqual(event.getMessage(), '"GET /casos/ HTTP/1.1" 200 1234')
