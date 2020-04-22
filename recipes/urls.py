from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('api/recipes/', views.RecipeListAPIView.as_view()),
    path(
        'recipes/<slug:slug>/',
        views.RecipeDetailView.as_view(),
        name='recipe-detail'
    )
]
