import logging


logger = logging.getLogger(__name__)


class MiddlewareLogger:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request from {request.user.id}")

        response = self.get_response(request)

        logger.info(f"Response with status {response.status_code} from {request.user.id} and URI {request.get_full_path()}")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info(f"Request from {request.user.id} to {view_func}({view_args}, {view_kwargs})")

    def process_exception(self, request, exception):
        logger.error(f"Response error {exception} from {request.get_full_path()}")
