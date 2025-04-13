from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MenuItem

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def cart(request):
    cart_items = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart_items.values())
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {'name': item.name, 'price': item.price, 'quantity': 1}

    request.session['cart'] = cart
    messages.success(request, f'{item.name} added to cart!')
    return redirect('menu')

@login_required
def order(request):
    request.session.pop('cart', None)
    messages.success(request, 'Order placed successfully!')
    return render(request, 'order.html')

def order_now(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name': item.name,
            'price': item.price,
            'quantity': 1
        }

    request.session['cart'] = cart
    messages.success(request, f"{item.name} added to your order!")
    return redirect('cart')
