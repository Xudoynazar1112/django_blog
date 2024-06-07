from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django_comments.forms import CommentForm
from django_comments.models import Comment

from .models import Post
from .forms import PostForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone


def home(request):
    latest_posts = Post.objects.filter(approved=True).order_by('-created_at')[:5]
    most_viewed_posts = Post.objects.filter(approved=True).order_by('-views')[:5]
    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)
    popular_week_posts = Post.objects.filter(approved=True, created_at__gte=week_ago).annotate(
        views_count=Count('views')).order_by('-views_count')[:5]
    popular_month_posts = Post.objects.filter(approved=True, created_at__gte=month_ago).annotate(
        views_count=Count('views')).order_by('-views_count')[:5]

    context = {
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
        'popular_week_posts': popular_week_posts,
        'popular_month_posts': popular_month_posts,
    }
    return render(request, 'home.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()

    content_type = ContentType.objects.get_for_model(post)
    comments = Comment.objects.filter(content_type=content_type, object_pk=post.pk, is_public=True)
    form = CommentForm(target_object=post)
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'content_type_id': content_type.id,
        'object_id': post.pk,
    }

    return render(request, 'post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
