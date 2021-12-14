from django.urls import path, include

from offices.views import BuildingView

urlpatterns = [
    path('/<int:building_id>', BuildingView.as_view()),
]
