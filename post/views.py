# coding: utf-8

from django.shortcuts import render, redirect
from math import ceil
from django.core.cache import cache

from post.models import Article, Comment


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
    return render(request, 'home.html', {'articles': articles,'pages':range(pages),'page':page})


# def article(request):
#     aid = int(request.GET.get('aid', 1))
#     article = Article.objects.get(id=aid)
#     comments = Comment.objects.filter(aid=aid)
#     return render(request, 'article.html', {'article': article, 'comments': comments})

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

  
# 查看帖子详情
def article(request):
    aid = int(request.GET.get('aid',1))

    key1 = 'article-%s'%aid
    key2 = 'comment-%s'%aid
    myarticle = cache.get(key1)
    comment = cache.get(key2)
    if myarticle is None:
        myarticle = Article.objects.get(id=aid)
        comment = Comment.objects.filter(aid=aid)
        cache.set(key2, comment, 3600)
        cache.set(key1,myarticle,3600)
        print('数据库查询文章')
    print('缓存查询')
    return render(request,'article.html',{'article':myarticle,'comments':comment})

  