from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class RedirectAuthenticatedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path in [reverse('register user'), reverse('login user')]:
                return redirect('home page')

        return response
