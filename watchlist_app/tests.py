from django.contrib.auth.models import User #imported from user_app models
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate

from watchlist_app.api import serializers
from watchlist_app import models


class OnlineLibraryTestCase(APITestCase):

    def setUp(self): # to login as a user
        self.user = User.objects.create_user(username = "testcase", password = "cft6yhn")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION ='Token ' + self.token.key)
        self.online = models.OnlineLibrary.objects.create(name = "LoveRead",
                    about = "The best free books store", website = "https://loveread.com")

    def test_onlinelibrary_create(self):
        data = {
            "name": "LoveRead",
            "about": "The best free books store",
            "website": "https://loveread.com"
        }
        response = self.client.post(reverse('library-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_onlinelibrary_list(self):
        response = self.client.get(reverse('library-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_onlinelibrary_ind(self):
        response = self.client.get(reverse('library-details', args = (self.online.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookTestCase(APITestCase):

    def setUp(self): # to login as a user
        self.user = User.objects.create_user(username = "testcase", password = "cft6yhn")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION ='Token ' + self.token.key)
        self.online = models.OnlineLibrary.objects.create(name = "LoveRead",
                    about = "The best free books store", website = "https://loveread.com")
        self.book = models.Book.objects.create(title = "Example",
                    storyline = "Example of consize description", platform = self.online, active = True)

    def test_book_create(self):
        data = {
            "title": "Example",
            "storyline": "Example of consize description",
            "platform": self.online,
            "active": True,
        } 
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_onlinelibrary_list(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_ind(self):
        response = self.client.get(reverse('book-details', args = (self.book.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Book.objects.count(), 1)
        self.assertEqual(models.Book.objects.get().title, 'Example') # we are accessing the book and then trying match its title


class ReviewTestCase(APITestCase):

    def setUp(self): # to login as a user
        self.user = User.objects.create_user(username = "testcase", password = "cft6yhn")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION ='Token ' + self.token.key)
        self.online = models.OnlineLibrary.objects.create(name = "LoveRead",
                    about = "The best free books store", website = "https://loveread.com")
        self.book = models.Book.objects.create(title = "Example",
                    storyline = "Example of description", platform = self.online, active = True)
        self.book2 = models.Book.objects.create(title = "Example2",
                    storyline = "Example of description2", platform = self.online, active = True)
        self.review = models.Review.objects.create(review_user = self.user, rating = 5,
                    description = "Good story!", book = self.book2, active = True,)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good story!",
            "book": self.book,
            "active": True,
        }
        response = self.client.post(reverse('review-create',args = (self.book.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        response = self.client.post(reverse('review-create',args = (self.book.id,)), data) # if someone trying add review for the second time
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_review_create_anon(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good story!",
            "book": self.book,
            "active": True,
        }       
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(reverse('review-create',args = (self.book.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Good story! - updated",
            "book": self.book,
            "active": True,
        }
        response = self.client.put(reverse('review-details',args = (self.book.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args = (self.book.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-details', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-details', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_review_user(self):
        response = self.client.get('/read/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
