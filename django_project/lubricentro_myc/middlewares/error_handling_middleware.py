import traceback

from lubricentro_myc.models.activity import UNHANDLED_EXCEPTION
from lubricentro_myc.utils import log_activity


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        log_activity(
            request,
            UNHANDLED_EXCEPTION,
            "Unhandled Exception Thrown",
            traceback.format_exc(),
        )
