from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)

from blogs.models import Blogs


class BlogsListView(ListView):
    model = Blogs

    def get_queryset(self):
        return Blogs.objects.filter(publication=True)


class BlogCreateView(CreateView):
    model = Blogs
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy("blogs:home_blogs")


class BlogDetailsView(DetailView):
    model = Blogs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj


class BlogUpdateView(UpdateView):
    model = Blogs
    fields = ('title', 'content', 'image')
    # success_url = reverse_lazy("blogs:home_blogs")
    def get_success_url(self):
        return reverse('blogs:details_blog', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blogs
    success_url = reverse_lazy("blogs:home_blogs")
