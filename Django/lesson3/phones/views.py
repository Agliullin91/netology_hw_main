from django.shortcuts import render

from phones.models import Phone


def show_catalog(request):
    sort = request.GET.get('sort')
    template = 'catalog.html'
    if sort == 'name':
        phone_objects = Phone.objects.order_by('name')
    elif sort == 'min_price':
        phone_objects = Phone.objects.order_by('price')
    elif sort == 'max_price':
        phone_objects = Phone.objects.order_by('-price')
    else:
        phone_objects = Phone.objects.all()
    context = {'phones': phone_objects,}
    return render(request, template, context)


def show_sorted_catalog_name(request):
    template = 'catalog.html'
    phone_sorted_list = Phone.objects.order_by('name')
    context = {'phones': phone_sorted_list,}
    return render(request, template, context)


def show_sorted_catalog_min(request):
    template = 'catalog.html'
    phone_sorted_list = Phone.objects.order_by('price')
    context = {'phones': phone_sorted_list,}
    return render(request, template, context)


def show_sorted_catalog_max(request):
    template = 'catalog.html'
    phone_sorted_list = Phone.objects.order_by('-price')
    context = {'phones': phone_sorted_list,}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_object = Phone.objects.filter(slug=slug)
    phone_model = [f'{i.name} costs {i.price}.' for i in phone_object]
    context = {'phone_model': phone_model}
    return render(request, template, context)
