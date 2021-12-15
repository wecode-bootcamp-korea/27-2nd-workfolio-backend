from django.urls import path, include

from offices.views import BuildingView, special_list

urlpatterns = [
    path('/<int:building_id>', BuildingView.as_view()),
    path('/specials', special_list),
]
