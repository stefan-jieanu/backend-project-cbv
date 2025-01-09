from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import CustomLoginView, CustomPasswordChangeView, SignUpView, welcome

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password', CustomPasswordChangeView.as_view(), name='change-password'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('welcome/', welcome, name='welcome')
]