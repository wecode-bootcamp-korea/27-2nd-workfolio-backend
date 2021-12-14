from django.urls import path, include

urlpatterns = [
    path('offices', include('offices.urls')),
]
