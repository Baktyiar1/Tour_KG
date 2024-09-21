from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    # path('register/', views.UserRegisterViews.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('profil/', views.UserProfilViews.as_view()),
    # path('logout/', views.UserLogoutView.as_view())
]
