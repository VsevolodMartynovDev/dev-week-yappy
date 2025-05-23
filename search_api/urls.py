from django.urls import path
from .views import SearchAPIView, search_view

urlpatterns = [
    path('api/search/', SearchAPIView.as_view(), name='api_search'),
    path('search/', search_view, name='search'),
] 