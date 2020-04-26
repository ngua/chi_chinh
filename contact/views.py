from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import generics
from .serializers import ContactSerializer


def contact(request):
    return render(request, 'contact/contact.html')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactSerializer
