from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('api/', views.RecipeListAPIView.as_view(), name='recipe-list'),
    path(
        '<int:year>/<int:month>/<slug:slug>/',
        views.RecipeDetailView.as_view(),
        name='recipe-detail'
    ),
    path(
        'archive/',
        views.RecipeArchiveView.as_view(),
        name='recipe-archive'
    ),
    path(
        'archive/<int:year>/<int:month>/',
        views.RecipeMonthArchiveView.as_view(month_format='%m'),
        name='recipe-month-archive'
    )
]
