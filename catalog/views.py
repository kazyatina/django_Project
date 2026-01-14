from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    return render(request, "catalog/contacts.html")


def post(request):
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    # return render(request, 'catalog/contacts.html')


def product_list(request):
    products2 = Product.objects.all()
    context = {
        "products2": products2,
    }
    return render(request, "catalog/product_list.html", context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context=context)


def main_page(request):
    products = Product.objects.all()
    context = {"products": products,}
    return render(request, 'catalog/main.html', context)

def form_to_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        print(name)
        description = request.POST.get('description')
        image = request.POST.get('image')
        price = request.POST.get('price')
        print(description)
        print(price)
        category = Category.objects.get(pk=request.POST.get('category'))
        print(category.name)
        Product.objects.create(name=name, description=description, image=image, price=price, category=category)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, "catalog/form.html",)