import json
import logging
from django.http import JsonResponse
from urllib.request import Request

from .exceptions import BadRequest, MethodNotAllowed

logger = logging.getLogger('app')

class SmallViewSet:
    def create(self, request: Request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    def list(self, request: Request, *args, **kwarg):
        raise MethodNotAllowed('GET')

    def retrieve(self, request: Request, pk, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def put(self, request: Request, pk, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def patch(self, request: Request, pk, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def delete(self, request: Request, pk, *args, **kwargs):
        raise MethodNotAllowed('DELETE')

    def parse_json_body(self, request: Request):
        if request.content_type != 'application/json':
            raise BadRequest('Invalid content type')
        return json.loads(request.body)

    def protect_create(self, request: Request):
        """
        Ensures that the request method is POST.
        Raises:
            MethodNotAllowed: If the request method is not GET.
        """
        if request.method != 'POST':
            raise MethodNotAllowed('POST')

    def protect_list(self, request: Request):
        """
        Ensures that the request method is GET.
        Raises:
            MethodNotAllowed: If the request method is not GET.
        """
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)

    def protect_retrieve(self, request: Request):
        """
        Ensures that the request method is GET.
        Raises:
            MethodNotAllowed: If the request method is not GET.
        """
        if request.method != 'GET':
            raise MethodNotAllowed(request.method)

    def protect_update(self, request: Request):
        """
        Ensures that the request method is PUT or PATCH.
        Raises:
            MethodNotAllowed: If the request method is not PUT or PATCH.
        """
        if request.method not in ['PUT', 'PATCH']:
            raise MethodNotAllowed(request.method)

    def protect_delete(self, request: Request):
        """
        Ensures that the request method is DELETE.
        Raises:
            MethodNotAllowed: If the request method is not DELETE.
        """
        if request.method != 'DELETE':
            raise MethodNotAllowed(request.method)

    def default_router(self, request: Request, pk=None, *args, **kwargs):
        """
        This method routes requests to the appropriate method based on the HTTP method and presence of a primary key (pk).
        
        It also handles errors and returns appropriate JSON responses by using the decorator @default_handle_endpoint_exceptions.
        
        GET/POST for collection endpoints and GET/PUT/PATCH/DELETE for detail endpoints.

        Example:
        ```
        # Note: AppViewSet is a subclass of SmallViewSet with overridden protect methods with more specific logic.

        class CommentViewSet(AppViewSet):
            def urlpatterns(self):
                return [
                    path('api/comments/',                     self.default_router, name='comments_collection'),
                    path('api/comments/<int:pk>/',            self.default_router, name='comments_detail'),
                    path('api/comments/<int:pk>/custom_put/', self.custom_put,     name='comments_custom_put_detail'),
                ]

            @default_handle_endpoint_exceptions
            def create(self, request: Request):
                self.protect_create(request)
                . . .

            @default_handle_endpoint_exceptions
            def update(self, request: Request, pk: int):
                self.protect_update(request)
                . . .

            @default_handle_endpoint_exceptions
            def custom_put(self, request: Request, pk: int):
                self.protect_update(request)
                . . .

            @disable_endpoint
            @default_handle_endpoint_exceptions
            def some_disabled_endpoint(self, request: Request):
                self.protect_retrieve(request)
                . . .
                
        ```
        """
        if pk is None:
            if request.method == 'GET':
                return self.list(request, *args, **kwargs)
            elif request.method == 'POST':
                return self.create(request, *args, **kwargs)
        else:
            if request.method == 'GET':
                return self.retrieve(request, pk, *args, **kwargs)
            elif request.method == 'PUT':
                return self.put(request, pk, *args, **kwargs)
            elif request.method == 'PATCH':
                return self.patch(request, pk, *args, **kwargs)
            elif request.method == 'DELETE':
                return self.delete(request, pk, *args, **kwargs)
        endpoint_type = "detail" if pk else "collection"
        logger.error(f'Got a none response from request_router for {endpoint_type} method {request.method}')
        return JsonResponse(data=None, safe=False, status=500)
