from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('register', views.RegisterNewUser, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('users_and_theirBooks',
         views.get_users_and_theirBooks, name="users_all_inf"),
    path('Mybooks', views.get_My_books, name="mybooks"),
    path('addBook', views.create_book, name="create_book"),
    path('find_poster/<str:pk>', views.find_poster, name="find_poster"),
    path('update/<str:pk>', views.update_book, name="update")

]
