from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Like
from .forms import PostForm, CommentForm


def home(request):
    return render(request, 'blog/insulthub.html')


def languages(request):
    return render(request, 'blog/languages.html')


def top(request):
    return render(request, 'blog/top.html')


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    liked = False

    if request.user.is_authenticated:
        liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
    })


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            like.delete()

    return redirect('post_detail', pk=post.pk)