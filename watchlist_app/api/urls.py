from django.urls import path, include
from watchlist_app.api.views import (BookAV, BookDetailAV, BookList,
                                     OnlineLibraryListAV, OnlineLibraryDetailAV, 
                                     ReviewList, ReviewDetail, ReviewCreate, UserReview)


urlpatterns = [
    path('list/', BookAV.as_view(), name='book-list'),
    path('list/<int:pk>/',  BookDetailAV.as_view(), name='book-details'),
    path('booklist/',  BookList.as_view(), name='booklist'),
   
    path('library/', OnlineLibraryListAV.as_view(), name='library-list'),
    path('library/<int:pk>/', OnlineLibraryDetailAV.as_view(), name='library-details'),
   
    path('<int:pk>/review/create/',  ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/',  ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/',  ReviewDetail.as_view(), name='review-details'),
    path('reviews/',  UserReview.as_view(), name='user-review-details'),
]