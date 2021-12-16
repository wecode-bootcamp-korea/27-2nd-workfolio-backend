from django.urls    import path, include

from users.views    import KakaoLogInView

urlpatterns = [
    path('/login', KakaoLogInView.as_view()) 
]