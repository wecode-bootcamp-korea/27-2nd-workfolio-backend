from django.urls import path

from offices.views import BuildingView, special_list, BuildingListView

urlpatterns = [
    path('', BuildingListView.as_view()),
    path('/<int:building_id>', BuildingView.as_view()),
    path('/specials', special_list),
]
