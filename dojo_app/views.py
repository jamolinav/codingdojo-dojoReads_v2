from collections import namedtuple
from typing import ContextManager
from django.db.models.expressions import OrderBy
from django.shortcuts import render, redirect
from .forms.dojo_app.user import UserForm, UserLoginForm
from .forms.dojo_app.book import BookForm
from django.contrib import messages
from dojo_app.models import *
from django.db.models import Avg, Count, Min, Sum, Q
from datetime import datetime, timezone, timedelta
from django.http import HttpResponse, JsonResponse, request
# Create your views here.

APP_NAME = 'dojo_app'
HOME = 'home_'+APP_NAME
def index(request):
    #return render(request, f'{APP_NAME}/index.html')
    return redirect(f'register_{APP_NAME}')
def register(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm()
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        print('va a register nuevo')
        return render(request, f'{APP_NAME}/register.html', context)
    
    if request.method == 'POST':
        print(request.POST)
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

        if User.ifExists(request.POST['email']):
            messages.error(request, 'Usuario ya existe')
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            request.session['logged_user'] = user.email
        else:
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, f'{APP_NAME}/register.html', context)

    return redirect('books')

def login(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
            }
        return render(request, f'{APP_NAME}/register.html', context)

    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            logged_user = loginForm.login(request.POST)
            if logged_user:
                request.session['logged_user_name'] = logged_user.first_name + ' ' + logged_user.last_name
                request.session['logged_user'] = logged_user.email
                print('logged_user: ', request.session['logged_user'])
                return redirect('books')
            
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        return render(request, f'{APP_NAME}/register.html', context)

def logout(request):
    try:
        del request.session['logged_user']
        del request.session['logged_user_name']
    except:
        print('Error')
    return redirect(HOME)

def books(request):
    if 'logged_user' not in request.session:
        return redirect(login)

    #Queryset:
    # k=Enrollment.objects.filter(course__courseid=1).values('id','course__courseid','course__name','enrollid')

    context = {
        'bookForm'  : BookForm(),
        'all_books' : Book.objects.all().order_by('id')[::-1],
        'books_last_review' : Book.objects.filter(reviews__in=Review.objects.all()).order_by('-reviews__updated_at')[:3],
        'others_books' : Book.objects.all(),
        'users' : User.objects.all(),
        'total_star' : range(5)
    }
    return render(request, f'{APP_NAME}/index.html', context)

def book(request, id_book):
    if 'logged_user' not in request.session:
        return redirect(login)

    books = Book.objects.filter(id=id_book)
    if len(books) != 1:
        messages.error(request, 'Libro no existe')
        return redirect(books)

    book = books[0]
    context = {
        'book'  : book,
        'all_review' : Review.objects.filter(book=book),
        'max_star'  : [0,1,2,3,4,5],
    }
    return render(request, f'{APP_NAME}/book.html', context)

def add_review(request):
    if 'logged_user' not in request.session:
        return redirect(login)

    if request.method == 'GET':
        return redirect('books')

    print(request.POST) 
    if 'id_book' not in request.POST:
        messages.error(request, 'Error al obtener libro')
        return redirect('books')

    id_book = request.POST['id_book']
    books = Book.objects.filter(id=id_book)
    if len(books) != 1:
        messages.error(request, 'Libro no existe')
        return redirect(books)

    book = books[0]

    errors = Review.objects.validator(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'book'  : book,
                'all_review' : Review.objects.filter(book=book),
                'max_star'  : [0,1,2,3,4,5],
                'data' : request.POST
            }
            return render(request,  f'{APP_NAME}/book.html', context)

    book.save()
    review = Review(review=request.POST['review'], book=book)
    review.save()

    context = {
                'book'  : book,
                'all_review' : Review.objects.filter(book=book),
                'max_star'  : [0,1,2,3,4,5],
            }
    return render(request,  f'{APP_NAME}/book.html')

def add_book(request):
    if 'logged_user' not in request.session:
        return redirect(login)
    
    if request.method == 'GET':
        context = {
            'max_star'  : [0,1,2,3,4,5],
            'all_books' : Book.objects.all().order_by('id')[::-1],
            'authors' : Author.objects.all(),
        }
        return render(request, f'{APP_NAME}/add_book.html', context)

    if request.method == 'POST':
        print(request.POST)
        errores = False

        fields_validate = ['title','new_author','review', 'raiting']
        for field in fields_validate:
            if not field in request.POST:
                messages.error(request, 'Falta definir campo: "' + field + '"')
                errores = True

        errors_author = {}
        errors_book = {}
        errors_review = {}

        errors_book = Book.objects.validator(request.POST)
        errors_review = Review.objects.validator(request.POST)
        errors_author= Author.objects.validator(request.POST)

        if len(errors_book) > 0 or len(errors_review) > 0 or len(errors_author) > 0:
            for key, value in errors_book.items():
                messages.error(request, value)
                errores = True
            for key, value in errors_review.items():
                messages.error(request, value)
                errores = True
            for key, value in errors_author.items():
                messages.error(request, value)
                errores = True
            
        if errores:
            print('NO grabar')
            context = {
                    'max_star'  : [0,1,2,3,4,5],
                    'all_books' : Book.objects.all().order_by('id')[::-1],
                    'authors' : Author.objects.all(),
                    'data' : request.POST,
                    } 

            return render(request, f'{APP_NAME}/add_book.html', context)

        else:

            print('grabar')
            
            author = Author.ifExists(request.POST['new_author'])
            author.save()

            book = Book(title=request.POST['title'], raiting=request.POST['raiting'], author=author)
            book.save()

            review = Review(review=request.POST['review'], book=book)
            review.save()

        return redirect('books')
    