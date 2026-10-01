from django.middleware.csrf import CsrfViewMiddleware
from django.test import RequestFactory, SimpleTestCase

from .views import save_message, save_test_result, submit_test


class WriteEndpointCsrfTests(SimpleTestCase):
    def test_json_write_endpoints_reject_missing_csrf_token(self):
        factory = RequestFactory()
        middleware = CsrfViewMiddleware(lambda request: None)

        for path, view in (
            ('/save-message/', save_message),
            ('/save-result/', save_test_result),
            ('/submit_test/example/', submit_test),
        ):
            with self.subTest(path=path):
                request = factory.post(path, data='{}', content_type='application/json')
                response = middleware.process_view(request, view, (), {})
                self.assertIsNotNone(response)
                self.assertEqual(response.status_code, 403)
