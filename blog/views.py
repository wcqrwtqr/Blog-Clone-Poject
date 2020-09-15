from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.urls import  reverse_lazy
# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')) # TOCHECK this is very possible to be wrong
    # for more details we can refer to the Field lookups in django  - Documentation

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html' # TOCHECK
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html' # TOCHECK
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DetailView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html' # TOCHECK the link later if its working or not
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')






