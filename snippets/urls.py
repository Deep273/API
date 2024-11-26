from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
   path('snippets/', views.snippet_list),
   path('snippets/<int:pk>/', views.snippet_detail),

]