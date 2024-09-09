from django.urls import path
from . import views

urlpatterns = [
    path('index/banner/', views.BannerIndexView.as_view()),
    path('index/regions/', views.RegionIndexView.as_view()),
    path('index/regions/<int:pk>/tours/', views.RegionListView.as_view()),
    path('index/tour_index/', views.TourIndexView.as_view()),

    path('index/create/', views.CreateTourView.as_view()),

    path('request_author/', views.TourAuthorRequestCreateView.as_view()),
    path('author_profile/', views.AuthorUserProfilViews.as_view()),

    path('rating/', views.AddStarRatingView.as_view()),

]
