from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import razorpay
from django.conf import settings



def place_order(request, total=0, quantity=0):
    current_user = request.user

    #Ensure user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    #Get cart items
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    # Calculate totals
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    #Handle POST
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user

            # Safe assignments
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.phone = form.cleaned_data.get('phone')
            data.email = form.cleaned_data.get('email')
            data.address_line_1 = form.cleaned_data.get('address_line_1')
            data.address_line_2 = form.cleaned_data.get('address_line_2')
            data.country = form.cleaned_data.get('country')
            data.state = form.cleaned_data.get('state')
            data.city = form.cleaned_data.get('city')
            data.order_note = form.cleaned_data.get('order_note')

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Safe fetch
            order = Order.objects.filter(
                user=current_user,
                is_ordered=False,
                order_number=order_number
            ).first()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                 "amount": int(grand_total * 100),  # amount in paise
                 "currency": "INR",
                 "payment_capture": "1"})
            order.order_number = razorpay_order['id']
            order.save()
            context = {
                 'order': order,
                 'cart_items': cart_items,
                 'total': total,
                 'tax': tax,
                 'grand_total': grand_total,
                 'razorpay_order_id': razorpay_order['id'],
                 'razorpay_key': settings.RAZORPAY_KEY_ID,
                 'amount': int(grand_total * 100),}
            return render(request, 'orders/payments.html', context)

        else:
            #IMPORTANT: show form errors
            print(form.errors)
            return redirect('checkout')

    return redirect('checkout')



from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

def payment_success(request):
    try:
        order = Order.objects.filter(user=request.user, is_ordered=False).last()

        # FAKE PAYMENT ENTRY
        payment = Payment.objects.create(
            user=request.user,
            payment_id="TEST12345",
            payment_method="COD / Fake",
            amount_paid=order.order_total,
            status="Completed"
        )

        # UPDATE ORDER
        order.payment = payment
        order.is_ordered = True
        order.status = "Completed"
        order.save()

        # MOVE CART → ORDER PRODUCTS
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True,
            )

            order_product.variations.set(item.variations.all())

        # CLEAR CART
        cart_items.delete()

        return redirect('order_success')

    except Exception as e:
        print("Error:", e)
        return redirect('checkout')
    


def order_success(request):
    order = Order.objects.filter(user=request.user, is_ordered=True).last()
    ordered_products = OrderProduct.objects.filter(order=order)
    context = {'order': order,
               'ordered_products': ordered_products,}
    return render(request,'orders/order_success.html',context)
    


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number, user=request.user)
    ordered_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'ordered_products': ordered_products,
    }
    return render(request, 'orders/order_detail.html', context)