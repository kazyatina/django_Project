import secrets

from dotenv import load_dotenv

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth import logout

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm, UserForm
from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser

load_dotenv(override=True)


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/users_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Пожалуйста, подтвердите свою регистрацию, перейдя по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        user = form.save()
        send_mail(
            subject="Добро пожаловать в наш сервис",
            message="Спасибо, что зарегистрировались в нашем сервисе!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def confirm_email(request, token):
    """Обработать подтверждение"""
    # Найти пользователя по токену
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


# Представление для выхода


def logout_view(request):
    logout(request)
    return redirect("catalog:product_list")


class UserListView(ListView):
    model = CustomUser
    template_name = "users/users_list.html"


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "users/user_detail.html"


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/users_form.html"

    def get_success_url(self):
        return reverse("users:user_detail", kwargs={"pk": self.object.pk})
