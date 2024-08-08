from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users-list'),
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='users-get'),
    path('users/update/<int:pk>/', UserUpdateAPIView.as_view(), name='users-update'),
    path('users/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='users-delete'),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
