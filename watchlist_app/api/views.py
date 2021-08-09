from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrreadOnly
from watchlist_app.models import Book, OnlineLibrary, Review
from watchlist_app.api.serializers import BookSerializer,OnlineLibrarySerializer, ReviewSerializer
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import BookPaginationPN, BookPaginationLO, BookPaginationCP
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username) #review_user is ForeignKey,  __username - jump to username to match it, in other case Foreign_key expected id


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ReviewCreateThrottle]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer): 
        pk = self.kwargs.get('pk')
        book = Book.objects.get(pk=pk)

        viewer = self.request.user
        review_queryset = Review.objects.filter(book=book,review_user=viewer)
       
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this book!")

        if book.number_rating == 0:
            book.avg_rating = serializer.validated_data['rating']
        else:
            book.avg_rating = ((book.avg_rating * book.number_rating) + serializer.validated_data['rating']) / (book.number_rating + 1)
        
        book.number_rating = book.number_rating + 1
        book.save()

        serializer.save(book=book,review_user=viewer)
     

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    #permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle, ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(book=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrreadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class OnlineLibraryVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = OnlineLibrary.objects.all()
    serializer_class = OnlineLibrarySerializer


class OnlineLibraryListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = OnlineLibrary.objects.all() #complex data
        serializer = OnlineLibrarySerializer(platform, many=True, context={"request":request}) # attribute many for list of objects
        return Response(serializer.data)

    def post(self, request):
        serializer = OnlineLibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class OnlineLibraryDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    serializer = OnlineLibrarySerializer()
    def get(self, request,pk):
        try:
            book = OnlineLibrary.objects.get(pk=pk)
        except OnlineLibrary.DoesNotExist:
            return Response({'ERROR':"Book not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = OnlineLibrarySerializer(book)
        return Response(serializer.data)

    def put(self, request,pk):
        book = OnlineLibrary.objects.get(pk=pk)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):     
        book = OnlineLibrary.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class BookList(generics.ListAPIView):
    queryset = Book.objects.all() #complex data
    serializer_class = BookSerializer     
    pagination_class = BookPaginationPN
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'avg_rating','storyline']
  

class BookAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        books = Book.objects.all() #complex data
        serializer = BookSerializer(books, many=True) # attribute many for list of objects
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class BookDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request,pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'ERROR':"Book not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request,pk):
        book = Book.objects.get(pk=pk) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):     
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
