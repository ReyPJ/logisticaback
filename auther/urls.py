from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import getCurrentUserView, getListUserView, deleteUserView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('current-user/', getCurrentUserView.as_view(), name='current_user'),
    path('list-user/', getListUserView.as_view(), name='list_user'),
    path('delete-user/<int:pk>/', deleteUserView.as_view(), name='delete_user'),
]
