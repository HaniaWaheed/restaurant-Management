from django.shortcuts import render
from .models import Table, MenuItem
from .models import Table, MenuItem, CartItem  # Added CartItem import
from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Order  # Assuming you have an Order model
from .forms import OrderStatusForm
from .models import Order
from .models import ReturnRequest, CustomerContact
from .forms import ReturnRequestForm, ContactForm
from .models import Payment
from .models import Order, Table  # Make sure to import your models
from .forms import PaymentForm
from decimal import Decimal
from django.contrib import messages

def index(request):
    tables = Table.objects.all()
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurant/index.html', {'tables': tables, 'menu_items': menu_items})

def admin_home(request):
    return render(request, 'restaurant/admin_home.html')

def contact(request):
    return render(request, 'restaurant/contact.html')


def order_management(request):
    return render(request, 'restaurant/order_management.html')

def sales_management(request):
    return render(request, 'restaurant/sales_management.html')

def food_management(request):
    return render(request, 'restaurant/food_management.html')

def add_to_cart(request):
    if request.method == "POST":
        pizza_name = request.POST.get('pizza_name')
        size = request.POST.get('size')
        
        # Retrieve cart from session or create a new one
        cart = request.session.get('cart', [])

        # Add the new item
        cart.append({'name': pizza_name, 'size': size})
        request.session['cart.html'] = cart  # Save back to session

        return redirect('cart.html')  # Redirect to cart page

# Display cart items
def cart(request):
    cart_items = request.session.get('cart', [])
    total = 0
    for item in cart_items:
        # Extract price from the size string
        price = int(item['size'].split('PKR ')[1])
        total += price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def login_management(request):
    if request.method == 'POST':
          pass
    return render(request, 'restaurant/login_management.html')

def pizza(request):
    return render(request, 'restaurant/pizza.html')


def burger(request):
    return render(request, 'restaurant/burger.html')

def panini(request):
    return render(request, 'restaurant/panini.html')

def drinks(request):
    return render(request, 'restaurant/drinks.html')

def sweet(request):
    return render(request, 'restaurant/sweet.html')

def roll(request):
    return render(request, 'restaurant/roll.html')

def sales_tracking(request):
    return render(request, 'restaurant/sales_tracking.html')


def Rating(request):
    return render(request, 'restaurant/Rating.html')


def feedback(request):
    return render(request, 'restaurant/feedback.html')


from django.shortcuts import render

def reports(request):
    sales_data = [
        {'date': '2025-02-21', 'total_sales': 5000},
        {'date': '2025-02-22', 'total_sales': 6000},
    ]
    top_item = "Pizza"  

    return render(request, 'restaurant/reports.html', {  # ✅ Ensure the template name matches
        'sales_data': sales_data,
        'top_item': top_item,
    })

def tax_record(request):
    tax_data = [
        {'date': '2025-02-21', 'total_orders': 20, 'tax_collected': 500},
        {'date': '2025-02-22', 'total_orders': 25, 'tax_collected': 650},
    ]
    total_tax = sum(record['tax_collected'] for record in tax_data)
    total_orders = sum(record['total_orders'] for record in tax_data)

    return render(request, 'restaurant/tax_record.html', {  # ✅ Ensure the template name matches
        'tax_data': tax_data,
        'total_tax': total_tax,
        'total_orders': total_orders,
    })

def order_capture(request):
    return render(request, 'restaurant/order_capture.html')

# Handle form submission
def submit_order(request):
    if request.method == 'POST':
        try:
            # Get form data
            customer_name = request.POST.get('customer_name')
            order_items = request.POST.get('order_items')
            order_total = request.POST.get('order_total')
            table_number = request.POST.get('table')  # Assuming you have a table select in your form

            # Validate required fields
            if not all([customer_name, order_items, order_total, table_number]):
                messages.error(request, "Please fill in all required fields")
                return redirect('order_capture')

            # Convert to decimal
            order_total = Decimal(order_total)

            # Get table instance
            table = Table.objects.get(number=table_number)

            # Create and save order
            order = Order.objects.create(
                customer_name=customer_name,
                order_items=order_items,
                order_total=order_total,
                table=table,
                status='received'  # Initial status
            )

            # Redirect to payment processing
            return redirect('process_payment', order_id=order.id)

        except (ValueError, Table.DoesNotExist) as e:
            messages.error(request, f"Error processing order: {str(e)}")
            return redirect('order_capture')
    
    # If not POST, redirect to order capture page
    return redirect('order_capture')
    

# Display order processing page
def order_processing(request):
    orders = Order.objects.all()  # Fetch all orders from the database
    return render(request, 'restaurant/order_processing.html', {'orders': orders})

# Update order status to 'Completed'
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = 'Completed'
        order.save()
        return redirect('order_processing')
    
def inventory_management(request):
    return render(request, 'restaurant/inventory_management.html')  # Rendering the template

completed_orders = [
    {'order_id': 'ORD001', 'customer_name': 'John Doe', 'items': ['Pizza', 'Coke'], 'status': 'Completed'},
    {'order_id': 'ORD002', 'customer_name': 'Jane Smith', 'items': ['Burger', 'Fries'], 'status': 'Completed'},
    {'order_id': 'ORD003', 'customer_name': 'Alice Brown', 'items': ['Pasta', 'Salad'], 'status': 'Completed'},
]
def order_fulfillment(request):
    total_completed_orders = len(completed_orders)
    context = {
        'completed_orders': completed_orders,
        'total_completed': total_completed_orders
    }
    return render(request, 'restaurant/order_fulfillment.html', context)


def order_capture(request):
    if request.method == 'POST':
        # Add your order creation logic here
        pass
    return render(request, 'restaurant/order_capture.html')

def order_tracking(request):
    today = date.today()
    orders = Order.objects.filter(timestamp__date=today)
    return render(request, 'restaurant/order_tracking.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
    else:
        form = OrderStatusForm(instance=order)
    
    return render(request, 'restaurant/order_detail.html', {
        'order': order,
        'form': form
    })


def customer_communication(request):
    contacts = CustomerContact.objects.all().order_by('-created_at')
    return render(request, 'restaurant/customer_communication.html', {'contacts': contacts})

def return_processing(request):
    returns = ReturnRequest.objects.all().order_by('-created_at')
    return render(request, 'restaurant/return_processing.html', {'returns': returns})

def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_communication')
    else:
        form = ContactForm()
    return render(request, 'restaurant/customer_communication.html', {'form': form})

def process_return(request, return_id):
    return_request = get_object_or_404(ReturnRequest, id=return_id)
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST, instance=return_request)
        if form.is_valid():
            form.save()
            return redirect('return_processing')
    else:
        form = ReturnRequestForm(instance=return_request)
    return render(request, 'restaurant/return_processing.html', {
        'form': form,
        'return_request': return_request
    })


def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.amount = order.order_total
            payment.save()
            
            # Update order status
            order.status = 'completed'
            order.save()
            
            return redirect('payment_success', payment_id=payment.id)
    else:
        initial = {'amount': order.order_total}
        form = PaymentForm(initial=initial)
    
    return render(request, 'restaurant/payment_form.html', {
        'form': form,
        'order': order
    })

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'restaurant/payment_success.html', {'payment': payment})

def billing_overview(request):
    payments = Payment.objects.all().order_by('-created_at')
    return render(request, 'restaurant/billing.html', {'payments': payments})

def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'restaurant/payment_detail.html', {'payment': payment})