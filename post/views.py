# coding: utf-8

from django.shortcuts import render, redirect
from math import ceil
from django.core.cache import cache


from post.models import Article, Comment, Users
from post.helper import page_cache, record_cilck, get_top_n_artivle

@page_cache(3)
def home(request):
    # 文章数量
    a_count = Article.objects.all().count()
    # 向上取整  显示页数
    pages = ceil(a_count / 5)
    # 获取当前页数
    page = int(request.GET.get('page',1))
    page=0 if page<1 else (page-1)

    start = page * 5
    end = start + 5
    articles = Article.objects.all()[start:end]

    # 访问数top10
    top10 = get_top_n_artivle(10)

    return render(request, 'home.html', {'articles': articles,'pages':range(pages),'page':page,'top10':top10})

# 查看帖子详情
@page_cache(5)
def article(request):
    aid = int(request.GET.get('aid', 1))
    article = Article.objects.get(id=aid)
    comments = Comment.objects.filter(aid=aid)
    # 记录文章点击量
    record_cilck(aid)
    return render(request, 'article.html', {'article': article, 'comments': comments})

# 创建帖子
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)
        return redirect('/post/article/?aid=%s' % article.id)
    else:

        return render(request, 'create.html')


def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article})

# 评论
def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')

# 查找
def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})

def top_ten(request):
    pass


#   注册
def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            users = Users.objects.create(name=name,password=password,email=email)
            print("************")
        except Exception as e:
            print(e)
        return redirect('/post/home/')
    else:
        return render(request,'user/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(name=username)
        if len(user) > 0:
            pwd = Users.objects.filter(password=password)
            if  len(pwd) > 0:
                # cache.set('username',username)
                return redirect('/post/home/',{'username':username})
            context =  {'error2': '密码输入错误'}
            return render(request, 'user/login.html', context=context)
        context = {'error1': '用户名输入错误'}
        return render(request,'user/login.html',context=context)
    else:
        return render(request,'user/login.html')







