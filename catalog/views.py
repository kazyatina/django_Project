from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Product, Category
from catalog.forms import ProductForm, CheckboxForm, ProductsModeratorForm, ModerationProductForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


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

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.owner != request.user:
    #         return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")
    #     if request.user.has_perm('catalog.can_unpublish_product'):
    #         return ProductsModeratorForm
    #     return super().post(request, *args, **kwargs)

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
