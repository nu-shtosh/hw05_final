from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post, User
from yatube.settings import PAGE_COUNT


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'posts': posts}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'group': group, 'posts': posts, 'page': page}
    return render(request, 'posts/group.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.author_posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'page': page}
    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author).exists():
        context['following'] = True
    return render(request, 'posts/profile.html', context)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    comments = post.post_comments.all()
    context = {
        'author': author,
        'post': post,
        'comments': comments,
        'form': form}
    if request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author).exists():
        context['following'] = True
    return render(request, 'posts/post.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if request.method == 'POST' and form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect(
            'post',
            username=request.user.username,
            post_id=post_id)
    return render(request, 'posts/new.html',
                  {'form': form, 'profile': profile, 'post': post})


@login_required
def add_comment(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post', username=username, post_id=post_id)
    context = {
        'author': author,
        'post': post,
        'form': form,
    }
    return render(request, 'posts/post.html', context)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'posts': posts}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=request.user)
    if Follow.objects.filter(author_id=author.id,
                             user_id=user.id).exists():
        return redirect('profile', username=username)
    if user != author:
        Follow.objects.create(author_id=author.id, user_id=user.id)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=request.user)
    if user != author:
        Follow.objects.filter(author_id=author.id,
                              user_id=user.id).delete()
    return redirect('profile', username=username)
