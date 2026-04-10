from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

'''def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method=='POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,variation__value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart= Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    try:
        cart_item= CartItem.objects.get(product=product,cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.quantity+=1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item= CartItem.objects.create(
            product= product,
            quantity=1,
            cart= cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()

    
    return redirect('cart') '''

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    # 🔹 Get variations from POST
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value   # ✅ FIXED FIELD NAME
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # =========================================================
    # 🔥 LOGGED-IN USER LOGIC
    # =========================================================
    if request.user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=request.user).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=request.user)

            existing_variations_list = []
            cart_item_ids = []

            for item in cart_items:
                existing_variations = list(item.variations.all())
                existing_variations_list.append(existing_variations)
                cart_item_ids.append(item.id)

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = cart_item_ids[index]
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    user=request.user
                )
                if len(product_variation) > 0:
                    cart_item.variations.set(product_variation)
                cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user
            )
            if len(product_variation) > 0:
                cart_item.variations.set(product_variation)
            cart_item.save()

        return redirect('cart')

    # =========================================================
    # 🔥 GUEST USER (SESSION CART)
    # =========================================================
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)

            existing_variations_list = []
            cart_item_ids = []

            for item in cart_items:
                existing_variations = list(item.variations.all())
                existing_variations_list.append(existing_variations)
                cart_item_ids.append(item.id)

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = cart_item_ids[index]
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart
                )
                if len(product_variation) > 0:
                    cart_item.variations.set(product_variation)
                cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation) > 0:
                cart_item.variations.set(product_variation)
            cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')





def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+= (cart_item.product.price* cart_item.quantity)
            quantity+=cart_item.quantity
        tax= (2*total)/100
        grand_total= total+tax

    except ObjectDoesNotExist:
        pass

    context={'total':total,
             'quantity':quantity,
             'cart_items':cart_items,
             'tax':tax,
             'grand_total':grand_total,
             }

    return render(request,'cart.html',context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'checkout.html', context)
