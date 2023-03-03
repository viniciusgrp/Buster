from django.urls import path
from . import views
from rest_framework_simplejwt import views as views_jwt

urlpatterns = [
    path("users/", views.AccountView.as_view()),
    path("users/login/", views.LoginJWTView.as_view()),
    path("token/refresh/", views_jwt.TokenRefreshView.as_view()),
    path("users/<int:user_id>/", views.AccountDetailView.as_view())
]
