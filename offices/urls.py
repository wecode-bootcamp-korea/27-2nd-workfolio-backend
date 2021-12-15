from django.urls import path, include

from offices.views import BuildingView, PlaceListView

urlpatterns = [
    path('/<int:building_id>', BuildingView.as_view()),
    path('/places', PlaceListView.as_view()),
]
