from django.urls import path
from catalog.views import home, contacts, post, product_list, product_detail, main_page, form_to_add_product
app_name = "catalog"  # пространство имен, всегда указывать для связки

# urlpatterns = [  # Маршруты связывают адреса с контролерами
#     path('show_data/', views.show_data, name='show_data'),
#     # Позволяет регистрировать наш маршрут (это части URL, которые будут использоваться для доступа к маршруту.
#     # Функции-контроллеры, которые будут выполнены при обращении к указанным путям.
#     # Имена маршрутов, которые можно использовать в шаблонах или при перенаправлении)
#     path('submit_data/', views.submit_data, name='submit_data'),
#     path('item/int:<item_id>/', views.show_item, name='show_item'),
# ]

urlpatterns = [  # Маршруты связывают адреса с контролерами
    path("", main_page, name='main_page'),
    path("home/", home, name="home"),
    # после создания маршрута нужно зарегить его в config urls
    path("contacts/", contacts, name="contacts"),
    path("post/", post, name="post"),
    path("form/", form_to_add_product, name="form"),
    path("product_list/", product_list, name="product_list"),
    path("product_detail/<int:pk>/", product_detail, name="product_detail"),

]

