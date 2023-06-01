from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from first.models import Post, Comment, Userlogin
from first.forms import (
    PostForm,
    PostDeleteConfirmForm,
    CommentForm,
    CommentDeleteConfirmForm,
)
def post_list(request):

    posts = Post.objects.prefetch_related("tags")
    if "tag_id" in request.GET:
        posts = posts.filter(tags__id=request.GET["tag_id"])
        
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, '文章建立成功')
        return redirect('post_list')

    return render(request, 'post_create.html', {'form': form})

def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, '文章編輯成功')
        return redirect('post_detail', post_id)

    return render(request, 'post_update.html', {'form': form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostDeleteConfirmForm(request.POST or None)
    if form.is_valid():
        post.delete()
        messages.success(request, '文章刪除成功')
        return redirect('post_list')

    return render(request, 'post_delete.html', {'form': form})

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        messages.success(request, "留言成功")
        return redirect("post_detail", post_id)

    return render(request, "post_comment.html", {"form": form})

def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save()
        messages.success(request, "留言編輯成功")
        return redirect("post_detail", comment.post_id)

    return render(request, "comment_update.html", {"form": form})


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    form = CommentDeleteConfirmForm(request.POST or None)
    if form.is_valid():
        comment.delete()
        messages.success(request, "留言刪除成功")
        return redirect("post_detail", comment.post_id)

    return render(request, "comment_delete.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "註冊帳號成功")
            return redirect('post_list')  # 將此行修改為你的視圖名稱或URL
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) #我們使用了 AuthenticationForm 表單來處理登入的相關表單驗證和登入操作。
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            # 使用 Django 內建的 authenticate 函數進行驗證
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # 使用 Django 內建的 login 函數進行登入
                login(request, user)
                if remember_me:
                    request.session.set_expiry(0)  # 設定 session 永久保存
                else:
                    request.session.set_expiry(120)  # 設定 session 120 秒後過期
                messages.success(request, "登入成功")
                return redirect('post_list')
            else:
                messages.error(request, "登入失敗，請檢查用戶名和密碼")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})