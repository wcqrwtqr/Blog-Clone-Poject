from django.shortcuts import render, get_object_or_404,redirect
from django.utils import  timezone
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


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = form.save(commit=False)
            Comment.post = post
            Comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blob/comment_form.html', {'form':form})


@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)





