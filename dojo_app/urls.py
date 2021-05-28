from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_dojo_app'),
    path('register', views.register, name='register_dojo_app'),
    path('login', views.login, name='login_dojo_app'),
    path('logout', views.logout, name='logout_dojo_app'),

    path('books', views.books, name='books'),
    path('add_book', views.add_book, name='add_book'),
    path('book/<int:id_book>', views.book, name='book'),
    path('add_review', views.add_review, name='add_review'),
    path('user/<int:user_id>', views.user, name='user'),
    path('delete_review/<int:review_id>', views.delete_review, name='delete_review'),
]