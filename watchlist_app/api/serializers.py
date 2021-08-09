from rest_framework import serializers
from watchlist_app.models import Book, OnlineLibrary, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
     
    class Meta:
         model = Review
         exclude = ('book',)
         #fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True) #impossible add review for Book - only from Review
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = Book
        fields = "__all__"
        #fields = ['name','description','active']
        #exclude = ['id']


class OnlineLibrarySerializer(serializers.ModelSerializer):

    book = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='book-details')

    class Meta:
        model = OnlineLibrary
        fields = "__all__"



