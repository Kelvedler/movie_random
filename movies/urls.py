from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieList.as_view()),
    path('<int:pk>/', views.MovieDetail.as_view()),
    path('genres/', views.GenreList.as_view()),
    path('genres/<int:pk>/', views.GenreDetail.as_view()),
    path('reviews/movie=<int:movie_id>/', views.MovieReviewList.as_view()),
]
