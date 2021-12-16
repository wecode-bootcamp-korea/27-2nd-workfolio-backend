from django.urls import path, include

urlpatterns = [
    path('buildings', include('offices.urls')),
    path('reservations', include('reservations.urls')),
    path('users', include('users.urls')),
]
