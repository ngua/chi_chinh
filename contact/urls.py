from django.urls import path
from . import views


urlpatterns = [
    path('', views.contact, name='contact'),
    path('api/', views.ContactCreateAPIView.as_view(), name='contact-endpoint'),
]
