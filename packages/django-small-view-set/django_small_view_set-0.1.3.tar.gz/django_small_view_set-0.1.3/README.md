# Django Small View Set

A lightweight Django ViewSet alternative with minimal abstraction. This library provides a simple and transparent way to define API endpoints without relying on complex abstractions.

## Getting Started with Django Small View Set

This guide provides a simple example to get started with the library.

### Example Usage

Here’s how you can define a basic API endpoint with one collection route and one detail route:

```python
from django.http import JsonResponse
from django.urls import path
from small_view_set.small_view_set import SmallViewSet
from small_view_set.decorators import default_handle_endpoint_exceptions

class BarViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/bars/',          self.default_router, name='bars_collection'),
            path('api/bars/<int:pk>/', self.default_router, name='bars_detail'),
        ]

    @default_handle_endpoint_exceptions
    def list(self, request, *args, **kwargs):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)

    @default_handle_endpoint_exceptions
    def retrieve(self, request, pk, *args, **kwargs):
        self.protect_retrieve(request)
        return JsonResponse({"message": f"Detail for ID {pk}"}, status=200)
```


## Registering in `urls.py`

To register the viewset in your `urls.py`:

```python
from api.views.bar import BarViewSet

urlpatterns = [
    # Other URLs like admin, static, etc.

    *BarViewSet().urlpatterns(),
]
```


## Documentation

- [Custom Endpoints](./README_CUSTOM_ENDPOINT.md): Learn how to define custom endpoints alongside the default router.
- [Handling Endpoint Exceptions](./README_HANDLE_ENDPOINT_EXCEPTIONS.md): Understand how to write your own decorators for exception handling.
- [Custom Protections](./README_CUSTOM_PROTECTIONS.md): Learn how to subclass `SmallViewSet` to add custom protections like logged-in checks.
- [DRF Compatibility](./README_DRF_COMPATIBILITY.md): Learn how to use some of Django Rest Framework's tools, like Serializers.
- [Reason](./README_REASON.md): Reasoning behind this package.
