import logging
from django.conf import settings
from functools import wraps

import json
import functools
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation, PermissionDenied
from django.http import (
    Http404,
    JsonResponse,
)

from .exceptions import EndpointDisabledException, MethodNotAllowed, Unauthorized


def _get_logger(name):
    """
    Retrieves a logger by name. If no logger is configured in settings.LOGGING,
    it provides a fallback logger with a StreamHandler.

    To control this logger in `settings.py`, add a logger configuration
    under the `LOGGING` dictionary. For example:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django-small-view-set.default_handle_endpoint_exceptions': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }

    This configuration ensures that the logger named
    'django-small-view-set.default_handle_endpoint_exceptions' uses the specified
    handlers and logging level.
    """
    logger = logging.getLogger(name)

    # Check if Django's logging is configured
    if not logger.hasHandlers():
        # Fallback logger setup
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def default_handle_endpoint_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = _get_logger('django-small-view-set.default_handle_endpoint_exceptions')

        try:
            return func(*args, **kwargs)

        except json.JSONDecodeError:
            return JsonResponse(data={"errors": "Invalid JSON"}, status=400)

        except (TypeError, ValueError) as e:
            if hasattr(e, 'detail'):
                return JsonResponse(data={'errors': e.detail}, status=400)
            if hasattr(e, 'message'):
                return JsonResponse(data={'errors': e.message}, status=400)
            return JsonResponse(data=None, safe=False, status=400)

        except Unauthorized:
            return JsonResponse(data=None, safe=False, status=401)

        except (PermissionDenied, SuspiciousOperation):
            return JsonResponse(data=None, safe=False, status=403)

        except (EndpointDisabledException, Http404, ObjectDoesNotExist):
            return JsonResponse(data=None, safe=False, status=404)

        except MethodNotAllowed as e:
            return JsonResponse(
                data={'errors': f"Method {e.method} is not allowed"},
                status=405)

        except Exception as e:
            # Catch-all exception handler for API endpoints.
            # 
            # - Always defaults to HTTP 500 with "Internal server error" unless the exception provides a more specific status code and error details.
            # - Duck types to extract error information from `detail` or `message` attributes, if available.
            # - Never exposes internal exception contents to end users for 5xx server errors unless settings.DEBUG is True.
            # - Allows structured error payloads (string, list, or dict) without assumptions about the error format.
            # - Logs exceptions fully for server-side diagnostics, distinguishing handled vs unhandled cases.
            # 
            # This design prioritizes API security, developer debugging, and future portability across projects.

            status_code = getattr(e, 'status_code', 500)
            error_contents = None

            if hasattr(e, 'detail'):
                error_contents = e.detail
            elif hasattr(e, 'message') and isinstance(e.message, str):
                error_contents = e.message

            if 400 <= status_code <= 499:
                if status_code == 400:
                    message = 'Bad request'
                elif status_code == 401:
                    message = 'Unauthorized'
                elif status_code == 403:
                    message = 'Forbidden'
                elif status_code == 404:
                    message = 'Not found'
                elif status_code == 405:
                    message = 'Method not allowed'
                elif status_code == 429:
                    message = 'Too many requests'
                elif error_contents:
                    message = error_contents
                else:
                    message = 'An error occurred'

                if settings.DEBUG and error_contents:
                    message = error_contents
            else:
                status_code = 500
                message = 'Internal server error'
                if settings.DEBUG:
                    message = error_contents if error_contents else str(e)

            func_name = func.__name__
            e_name = type(e).__name__
            if error_contents:
                msg = f"Handled API exception in {func_name}: {e_name}: {error_contents}"
                logger.error(msg)
                    
            else:
                msg = f"Unhandled exception in {func_name}: {e_name}: {e}"
                logger.error(msg)
                    

            return JsonResponse(
                data={'errors': message},
                safe=False,
                status=status_code,
                content_type='application/json')

    return wrapper


def disable_endpoint(view_func):
    """
    Temporarily disables an API endpoint based on the SMALL_VIEWSET_RESPECT_DISABLED_ENDPOINTS setting.

    When `SMALL_VIEWSET_RESPECT_DISABLED_ENDPOINTS` in Django settings is set to `True`, this decorator
    will raise an `EndpointDisabledException`, resulting in a 404 response. When set to `False`,
    the endpoint will remain active, which is useful for testing environments.

    Usage:
        - Apply this decorator directly to a view method or action.
        - Example:
        
        ```python
        class ExampleViewSet(SmallViewSet):

            @disable_endpoint
            @default_handle_endpoint_exceptions
            def retrieve(self, request: Request) -> JsonResponse:
                self.protect_retrieve(request)
                . . .
        ```
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if settings.SMALL_VIEWSET_RESPECT_DISABLED_ENDPOINTS:
            raise EndpointDisabledException()
        return view_func(*args, **kwargs)
    return wrapper

