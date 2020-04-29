from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecipeSearchListView.as_view(), name='search'),
]
