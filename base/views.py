from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import registerationForm
from .models import Cart, Category, Product, SoldOutItem, User
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import datetime
import os
from django.http import HttpResponse
from django.utils.encoding import smart_str
import base64
from django.contrib import messages

# /////##
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def create_checkout_pdf(file_path, checkout_details):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    def draw_header():
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Checkout Summary")

        c.setFont("Helvetica-Bold", 12)
        headers = ["Product", "Quantity", "Price per Unit", "Total Price"]
        x_positions = [1 * inch, 3 * inch, 4 * inch, 5.5 * inch]

        for i, header in enumerate(headers):
            c.drawString(x_positions[i], height - 1.5 * inch, header)

    draw_header()

    y_position = height - 2 * inch
    total_price_all_products = 0
    line_height = 0.5 * inch

    c.setFont("Helvetica", 12)
    for item in checkout_details:
        if y_position < 1 * inch:  
            c.showPage()  
            draw_header()  
            y_position = height - 2 * inch 

        product = item['product']
        quantity = item['quantity']
        price = item['price']
        total_price = item['total_price']
        total_price_all_products += total_price

        c.drawString(1 * inch, y_position, product)
        c.drawString(3 * inch, y_position, str(quantity))
        c.drawString(4 * inch, y_position, f"${price:.2f}")
        c.drawString(5.5 * inch, y_position, f"${total_price:.2f}")
        y_position -= line_height

    if y_position < 1 * inch: 
        c.showPage()
        draw_header()
        y_position = height - 2 * inch

    c.setFont("Helvetica-Bold", 12)
    c.drawString(4 * inch, y_position - line_height, "Total:")
    c.drawString(5.5 * inch, y_position - line_height, f"${total_price_all_products:.2f}")

    c.showPage()
    c.save()
    fileName = file_path
    return fileName



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password, '<---user authentiated')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)




def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = registerationForm()

    if request.method == "POST":
        form = registerationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print(user, '<----username')
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'base/profile.html', {'user': user})

def home_page(request):
    products = Product.objects.order_by('?')[:6]
    categories = Category.objects.all()
    banner = Product.objects.order_by('rate').order_by('?')[:3]

    # img = Product.objects.get(id=1).image.url
    # print(img)

    context = {'products': products, 'categories': categories, 'banner':banner}
    return render(request, 'base/home.html', context)


def productsPage(request):
    q = request.GET.get('q', '')

    if q:
        products = Product.objects.filter(Q(category__name__icontains=q))
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    context = {'products': products, 'categories': categories, 'q':q}
    return render(request, 'base/products.html', context)

def searchPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(category__name__icontains=q) |
        Q(description__icontains=q)
    )

    context = {'products': products}

    return render(request, 'base/search.html', context)


@login_required(login_url='login')
def cartPage(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart)
    context = {'carts': cart, 'total_price': total_price}
    return render(request, 'base/cart.html', context)


@login_required(login_url='login')
def addToCart(request, pk):
    product = Product.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(
        product=product,
        user=request.user
    )
    if not created:
        cart.quantity += 1
        cart.save()

    next_url = request.GET.get('next', reverse('home'))
    return redirect(next_url)


@login_required(login_url='login')
def updateQuantity(request, pk):
    if request.method == 'POST':
        cart = Cart.objects.get(id=pk, user=request.user)
        new_quantity = request.POST.get('quantity')
        cart.quantity = new_quantity
        cart.save()
        return redirect('cart-page')


@login_required(login_url='login')
def deleteFromCart(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        cart_item = get_object_or_404(Cart, id=id, user=request.user)
        cart_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)




@login_required(login_url='login')
def checkoutPage(request):
    if request.method == "POST":
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if cart_items.exists():
            checkout_details = []
            total_price = 0

            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity
                price = product.price
                total_price += quantity * price

                checkout_details.append({
                    'product': product.name,
                    'quantity': quantity,
                    'price': price,
                    'total_price': quantity * price
                })

            file_path = create_checkout_pdf(f"checkout/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
                                            checkout_details)

            with open(file_path, 'rb') as file:
                pdf_data = base64.b64encode(file.read()).decode('utf-8')

            os.remove(file_path)

            return JsonResponse({'pdf_data': pdf_data})

        else:
            return JsonResponse({'error': 'No items in the cart'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
