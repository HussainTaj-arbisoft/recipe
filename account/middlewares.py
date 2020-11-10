from django.contrib import auth
from django.contrib.auth.middleware import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AccountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(
            request, "session"
        ), "You must use the session middleware to use AccountMiddleware"
        request.user = SimpleLazyObject(lambda: get_user(request))