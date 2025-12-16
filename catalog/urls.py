from django.urls import path
from catalog.views import home, contacts, post

app_name = 'catalog'  # пространство имен, всегда указывать для связки

# urlpatterns = [  # Маршруты связывают адреса с контролерами
#     path('show_data/', views.show_data, name='show_data'),
#     # Позволяет регистрировать наш маршрут (это части URL, которые будут использоваться для доступа к маршруту.
#     # Функции-контроллеры, которые будут выполнены при обращении к указанным путям.
#     # Имена маршрутов, которые можно использовать в шаблонах или при перенаправлении)
#     path('submit_data/', views.submit_data, name='submit_data'),
#     path('item/int:<item_id>/', views.show_item, name='show_item'),
# ]

urlpatterns = [  # Маршруты связывают адреса с контролерами
    path('', home, name='home'),
    # после создания маршрута нужно зарегить его в config urls
    path('contacts/', contacts, name='contacts'),
    path('post/', post, name='post')]
