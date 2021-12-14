from django.urls import path, include

urlpatterns = [
    path('buildings', include('offices.urls')),
]
