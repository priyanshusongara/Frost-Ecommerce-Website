from django.db import models
from category.models import Category

from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique = True)
    slug = models.CharField(max_length=200, unique = True)
    description = models.CharField(max_length=100, unique = True)
    price = models.IntegerField(max_length=500, blank = True)
    images =  models.ImageField(upload_to="photos/products")
    stock= models.IntegerField()
    is_available=models.BooleanField(default=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
    )

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects=VariationManager()

    def __unicode__(self):
        return self.product
    

from django.shortcuts import render,get_object_or_404
from .models import Product
from .models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request,category_slug=None):
    categories=None
    products=None

    if category_slug!= None:
        categories= get_object_or_404(Category, slug=category_slug)
        products= Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator (products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count=products.count()

    context={'products': products,
             'product_count':product_count,}
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product= Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart= CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    context = {'single_product':single_product,
               'in_cart':in_cart,
               }

    return render(request,'product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products= Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()
    context = {'products': products,
               'product_count': product_count,
    }
    return render(request, 'store.html', context)


from django.db import models
from accounts.models import Account


class ReviewRating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
