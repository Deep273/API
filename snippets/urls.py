from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
   path('snippets/', views.snippet_list),
   path('snippets/<int:pk>/', views.snippet_detail),
   path('users/', views.user_list),  # GET для списка пользователей
   path('users/<int:pk>/', views.user_detail),  # GET, PUT, PATCH, DELETE для пользователя по id
]