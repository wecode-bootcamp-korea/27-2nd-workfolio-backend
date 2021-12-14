from django.urls import path, include

from offices.views import OfficeView

urlpatterns = [
    path('/<int:building_id>', OfficeView.as_view()),
]
