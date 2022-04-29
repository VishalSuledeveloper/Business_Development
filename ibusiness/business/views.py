from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, get_user_model, logout as django_logout
from django.contrib import messages

from .models import Post, Category

User = get_user_model()
# Create your views here
def home(request):
    # load all the post from db(10)
    posts = Post.objects.all()[:11]
    print(posts)

    cats = Category.objects.all()

    data = {
        'posts': posts,
        'cats': cats
    }
    return render(request, 'home.html', data)


def post(request, url):
    if request.user.is_anonymous:
        messages.add_message(request, messages.ERROR, 'Log in to view this page')
        return redirect('/login/')
    post = Post.objects.get(url=url)
    cats = Category.objects.all()

    # print(post)
    return render(request, 'post.html', {'post': post, 'cats': cats})


def category(request, url):
    cat = Category.objects.get(url=url)
    cats = Category.objects.all()
    posts = Post.objects.filter(cat=cat)
    return render(request, "category.html", {'cat': cat, 'cats': cats, 'posts': posts})


def login(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.add_message(request, messages.ERROR, 'Username and password are required')
    else:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Successfully logged in')
            return redirect('/home/')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid email or password')

    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    if request.method == 'GET':
        return render(request, 'register.html')

    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('username')

    if not email:
        messages.add_message(request, messages.ERROR, 'Email is required')
    if not username:
        messages.add_message(request, messages.ERROR, 'Missing username')
    if not password:
        messages.add_message(request, messages.ERROR, 'Password kidhar hai be')

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'User created successfully')
        return redirect('/login/')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)

    return render(request, 'register.html')


def logout(request):
    if request.user.is_anonymous:
        messages.add_message(request, messages.ERROR, 'You\'re not logged in')
        return redirect('/home/')
    django_logout(request)
    return redirect('/home/')
