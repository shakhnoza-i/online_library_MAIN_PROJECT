from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib .auth.models import User


class OnlineLibrary(models.Model): # one platform can encompase many books
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self): 
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(OnlineLibrary,on_delete=models.CASCADE,related_name="book") # one book can be at only one platfotm
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200,null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return str(self.rating) + " | " + self.book.title + " | " + str(self.review_user)