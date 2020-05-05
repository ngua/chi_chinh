from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from rest_framework import generics
from .serializers import ContactSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def contact(request):
    return render(request, 'contact/contact.html')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactSerializer
