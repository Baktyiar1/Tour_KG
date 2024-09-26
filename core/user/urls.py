from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    # path('register/', views.UserRegisterViews.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('profile/', views.UserProfilViews.as_view()),
    path('profile_booking/', views.UserBookingView.as_view()),

    path('profile_author/', views.AuthorToursView.as_view()),
    path('qrcode/<int:pk>/', views.QrCodeView.as_view()),
    path('booking_list/', views.AuthorBookingListView.as_view()),
    path('booking_status/<int:pk>/', views.ConfirmBookingView.as_view()),
    # path('logout/', views.UserLogoutView.as_view())
]
