from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blogs.views import (
    BlogsListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogDetailsView,
)

app_name = "blogs"

urlpatterns = [
    path("blogs/", BlogsListView.as_view(), name="home_blogs"),
    path("details_blog/<int:pk>/", BlogDetailsView.as_view(), name="details_blog"),
    path("create_blog/", BlogCreateView.as_view(), name="create_blog"),
    path("update_blog/<int:pk>/update/", BlogUpdateView.as_view(), name="update_blog"),
    path("delete_blog/<int:pk>/delete/", BlogDeleteView.as_view(), name="delete_blog"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)