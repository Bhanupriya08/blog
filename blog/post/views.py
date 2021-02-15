from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post,Category
from django.shortcuts import redirect
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'post/post_list.html', {"posts":posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/post_detail.html', {'post': post})




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {'form': form})


def category(request):
    catg = Category.objects.all()
    return render(request,'post/catg.html',{'catg':catg})

def cat_post(request,cats):
    category = Category.objects.filter(name=cats).first()
    print(category)
    posts = Post.objects.filter(category=category).all()
    return render(request,'post/catg_post.html',{'posts':posts})
