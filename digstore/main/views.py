from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProductForm
from .models import Product, Category
import random

def index(request):
    categories = Category.objects.all()
    category_filter = request.GET.getlist('category')
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    price_max = request.GET.get('price_max')
    rating_min = request.GET.get('rating_min')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass
    if rating_min:
        try:
            products = products.filter(rating__gte=float(rating_min))
        except ValueError:
            pass
    if sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'rating_desc':
            products = products.order_by('-rating')
        elif sort == 'created_at_desc':
            products = products.order_by('-created_at')

    products_by_category = {}
    for category in categories:
        category_products = products.filter(category=category)
        if category_filter and category.name not in category_filter:
            continue
        products_by_category[category] = category_products


    return render(request, 'main/index.html', {
        'title': 'Главная страница сайта',
        'products_by_category': products_by_category,
        'categories': categories,
        'popular_products': Product.objects.order_by('-sales_count')[:3]
    })

def about(request):
    return render(request, 'main/about.html')

@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Товар успешно создан!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка в форме. Пожалуйста, проверьте данные.')
    form = ProductForm()
    categories = Category.objects.all() 
    return render(request, 'main/create.html', {
        'form': form,
        'categories': categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_stats = product.get_seller_stats()
    return render(request, 'main/product_detail.html', {
        'title': product.name,
        'product': product,
        'seller_stats': seller_stats
    })

def purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.sales_count += 1
    product.save()
    combinations = [c.strip() for c in product.combinations.split(',') if c.strip()]
    combination = random.choice(combinations) if combinations else "Нет комбинаций"
    return render(request, 'main/purchase_success.html', {
        'title': 'Покупка успешна',
        'product': product,
        'combination': combination
    })

def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        product.update_rating(rating)
        messages.success(request, 'Спасибо за ваш отзыв!')
        return redirect('purchase', product_id=product.id)
    return redirect('product_detail', product_id=product_id)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'main/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Этот email уже зарегистрирован.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                messages.success(request, 'Регистрация успешна!')
                return redirect('home')
        else:
            messages.error(request, 'Пароли не совпадают.')
    return render(request, 'main/register.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')