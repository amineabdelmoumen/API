from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, BookSerializer, ProfilSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from datetime import datetime
from .models import User, Book, Profil
# Create your views here.


@api_view(['POST', ])
def RegisterNewUser(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data["success"] = "sucessfully register a new user"
        data['username'] = account.username
        data['email'] = account.email
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_My_books(request):  # the current user books
    user = request.user
    books = user.Books.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def create_book(request):  # let the current user to create book post
    book = request.data
    serializer = BookSerializer(
        data=book)
    data = {}
    if serializer.is_valid():
        # saving the book and attached to the current user(remember here we have a foreinkey)
        serializer.save(user=request.user, creation_time=datetime.now())
        data["success"] = "successufully adding the book"
        data["user_name"] = request.user.username
        return Response(data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def find_poster(request, pk):  # get the user who post a book with a given user id
    try:
        book = Book.objects.get(id=pk)
        poster = book.user
        serializer = UserSerializer(poster)
        return Response(serializer.data)
    except book.DoesNotExist:
        content = {'please move along': 'there is no book with that id'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])  # one Api call(the power of using a nested serializer)
@permission_classes([IsAuthenticated])
def get_users_and_theirBooks(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def update_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
        if request.user.id == book.user.id:
            book_serializer = BookSerializer(instance=book, data=request.data)
            if book_serializer.is_valid():
                book_serializer.save(user=request.user)
    except book.DoesNotExist:
        content = {'please move along': 'you are not the root'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
