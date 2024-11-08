from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment_Pos
from .forms import PostForm, CommentForm

# CRUD pour Post
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('list')

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)  # Récupère l'article avec l'ID spécifié
    return render(request, 'blog/detail.html', {'post': post})

# CRUD pour Comment
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('list')
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})
