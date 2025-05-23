from django.urls import path
from .views import SearchAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search'),
] 