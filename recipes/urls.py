from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('api/recipes/', views.RecipeListAPIView.as_view()),
    path(
        'recipes/<int:year>/<int:month>/<slug:slug>/',
        views.RecipeDetailView.as_view(),
        name='recipe-detail'
    ),
    path(
        'recipes/archive/',
        views.RecipeArchiveView.as_view(),
        name='recipe-archive'
    ),
    path(
        'recipes/archive/<int:year>/<int:month>/',
        views.RecipeMonthArchiveView.as_view(month_format='%m'),
        name='recipe-month-archive'
    )
]
