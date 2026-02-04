from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Product, Category
from catalog.forms import ProductForm, CheckboxForm, ProductsModeratorForm, ModerationProductForm
from catalog.services import get_list_products


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    # низкоуровневое кеширование списка продуктов
    def get_queryset(self):
        queryset = cache.get("products_queryset")
        if not queryset:
            queryset = super().get_queryset()
            cache.set('products_queryset', queryset, 1)  # Кешируем данные на 15 минут
        return queryset


# кеширование страницы отображения информации об одном продукте
@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    # context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'image', 'price', 'category')
    success_url = reverse_lazy("catalog:product_list")


    def form_valid(self, form):
        product = form.save()
        user = self.request.user  # Устанавливаем владельца на текущего пользователя
        product.owner = user
        product.save()
        return super().form_valid(form)

    def checkbox(request):
        form = CheckboxForm()
        return render(request, "product_form.html", {"form": form})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    # fields = ('name', 'description', 'image', 'price', 'category')

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def checkbox(request):
        form = CheckboxForm()
        return render(request, "product_form.html", {"form": form})

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductsModeratorForm
        return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)

        if not (request.user.has_perm('catalog.can_delete_product') or request.user == product.owner):
            return HttpResponseForbidden("У вас нет прав для удаления продукта.")

        product.delete()

        return redirect('catalog:product_list')


class ProductUnpublishView(View):
    form_class = ProductForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        if request.user.has_perm('catalog.can_unpublish_product'):
            product.status = 'unpublic'
            product.save()
            return redirect('catalog:products_list')
        else:
            return HttpResponseForbidden("У вас нет прав на выполнение этого действия.")



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


class ListProductsInCategory(DetailView):
    model = Category
    template_name = 'catalog/products_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context["categories"] = get_list_products(category_id)
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories'
