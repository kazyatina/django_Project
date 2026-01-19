from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Product, Category
from catalog.forms import ProductForm, CheckboxForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    # context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'image', 'price', 'category')
    success_url = reverse_lazy("catalog:product_list")

    def checkbox(request):
        form = CheckboxForm()
        return render(request, "product_form.html", {"form": form})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    # fields = ('name', 'description', 'image', 'price', 'category')

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def checkbox(request):
        form = CheckboxForm()
        return render(request, "product_form.html", {"form": form})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ContactPageView(TemplateView):
    model = Product
    template_name = "catalog/contacts.html"


def form_to_add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        print(name)
        description = request.POST.get("description")
        image = request.POST.get("image")
        price = request.POST.get("price")
        print(description)
        print(price)
        category = Category.objects.get(pk=request.POST.get("category"))
        print(category.name)
        Product.objects.create(
            name=name,
            description=description,
            image=image,
            price=price,
            category=category,
        )
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(
        request,
        "catalog/form.html",
    )
