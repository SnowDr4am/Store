from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
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
    if not request.session.get(f'purchased_{product_id}', False):
        product.sales_count += 1
        product.save()
        request.session[f'purchased_{product_id}'] = True
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

User = get_user_model()

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password1', '')
        password_confirm = request.POST.get('password2', '')

        errors = []

        if not username:
            errors.append('Введите имя пользователя')
        elif len(username) < 4:
            errors.append('Имя пользователя должно содержать минимум 4 символа')
        elif not username.isalnum():
            errors.append('Имя пользователя может содержать только буквы и цифры')
        elif User.objects.filter(username__iexact=username).exists():
            errors.append('Пользователь с таким именем уже существует')

        try:
            validate_email(email)
            if User.objects.filter(email__iexact=email).exists():
                errors.append('Этот email уже зарегистрирован')
        except ValidationError:
            errors.append('Введите корректный email адрес')

        if password != password_confirm:
            errors.append('Пароли не совпадают')
        else:
            if len(password) < 8:
                errors.append('Пароль должен содержать минимум 8 символов')
            if not any(char.isdigit() for char in password):
                errors.append('Пароль должен содержать хотя бы одну цифру')
            if not any(char.isalpha() for char in password):
                errors.append('Пароль должен содержать хотя бы одну букву')

        if not errors:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_active = True
                user.save()

                from django.contrib.auth import login
                login(request, user)

                messages.success(request, 'Регистрация успешна! Добро пожаловать!')
                return redirect('home')

            except Exception as e:
                errors.append('Произошла ошибка при создании аккаунта. Пожалуйста, попробуйте позже.')
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Registration error: {str(e)}")

        for error in errors:
            messages.error(request, error)

        request.session['register_form_data'] = {
            'username': username,
            'email': email,
        }

    form_data = request.session.pop('register_form_data', {})

    return render(request, 'main/register.html', {
        'username': form_data.get('username', ''),
        'email': form_data.get('email', ''),
    })

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')