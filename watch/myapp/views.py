from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CreativeSignupForm, CreativeLoginForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order, OrderItem
from django.contrib import messages
from .models import Product
from django.contrib.auth import logout
from django.shortcuts import redirect # Ensure this is imported
# Create your views here.
def index(request):
    return render(request,'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = CreativeSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in immediately after signup
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index') # Change 'home' to your desired redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreativeSignupForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CreativeLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') # Change 'home' to your homepage
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CreativeLoginForm()
        
    return render(request, 'login.html', {'form': form})

def catalog_view(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

# ... (keep your existing login/signup/home views here) ...

@login_required
def place_order(request):
    if request.method == 'POST':
        try:
            # 1. Parse JSON data sent from JavaScript
            data = json.loads(request.body)
            cart_items = data.get('items', [])
            total_price = data.get('total_price', 0)

            # 2. Create the Main Order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price
            )

            # 3. Create each Order Item
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    price=item['price'],
                    quantity=item['qty']
                )

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def logout_view(request):
    logout(request)
    # Change 'login' to 'signup' if you prefer redirecting there
    return redirect('login')