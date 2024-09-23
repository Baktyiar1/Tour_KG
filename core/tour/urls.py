from django.urls import path
from . import views

urlpatterns = [
    path('index/banner/', views.BannerIndexView.as_view()),
    path('index/regions/', views.RegionIndexView.as_view()),
    path('index/regions/<int:pk>/tours/', views.RegionListView.as_view()),
    path('index/tour_index/', views.TourIndexView.as_view()),

    path('author_create/', views.CreateTourView.as_view()),

    # заявка на авторство
    path('request_author/', views.TourAuthorRequestCreateView.as_view()),
    path('request_author_list/', views.AuthorTourRequesListView.as_view()),
    path('author_status/<int:pk>/', views.TourAuthorRequestStatusView.as_view()),
    path('author_status_list/', views.AuthorRequestStatusListView.as_view()),


    # path('author_profile/', views.AuthorUserProfilViews.as_view()),

    path('rating/', views.AddStarRatingView.as_view()),

    # избранный
    path('wishlist/', views.WishlistView.as_view()),

    # бронирования
    path('booking/', views.CreateBookingView.as_view()),

    # оплата
    path('payment/', views.PaymentView.as_view()),



    # детальная страница
    path('index/detail/<int:pk>/', views.TourDetailView.as_view()),
    path('reviews/', views.ReviewsCreateView.as_view())

]
