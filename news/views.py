from datetime import datetime, timedelta
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.models import Article, ArticleViews, Category
# Create your views here.

class HomeView(View):
    def get(self, request):
        articles = Article.objects.all()
        categories = Category.objects.all()

        latest_articles = articles[:5]
        popular_articles = articles.filter(popular=True)[:4]
        slider_articles = articles.filter(slider=True)[:10]
        
        qs = articles.exclude(video='')
        video = None
        if qs.exists():
            video = qs[0].video.url
        query_tags = sum(categories.exclude(search_params=None).values_list('search_params', flat=True), []) 

        context = {
            'latest_articles': latest_articles, 'popular_articles':popular_articles,
            'slider_articles': slider_articles, 'categories':categories, 'video': video, 
            'tags':query_tags
        }
        
        return render(request, 'news/home.html', context)

class AllArticlesView(ListView):
    model = Article
    template_name = 'news/all-articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AllArticlesView, self).get_context_data(**kwargs)
        categories = Category.objects.all()

        context['categories'] = categories
        qs = self.get_queryset().exclude(video='')
        context['video'] = None
        if qs.exists():
            context['video'] = qs[0].video.url
        context['tags'] = sum(categories.exclude(search_params=None).values_list('search_params', flat=True), []) 

        return context

class CategoryArticlesView(ListView):
    model = Article
    template_name = 'news/category-articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_object(self):
        try:
            category = Category.objects.get(slug=self.kwargs.get('category_slug'))
        except:
            raise Http404()
        return category

    def get_queryset(self):
        queryset = self.get_object().articles.select_related('category')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesView, self).get_context_data(**kwargs)
        categories = Category.objects.all()

        articles = self.get_queryset()
        context['category'] = self.get_object() 
        qs = articles.exclude(video='')
        context['video'] = None
        if qs.exists():
            context['video'] = qs[0].video.url
        context['categories'] = categories
        context['tags'] = sum(categories.exclude(search_params=None).values_list('search_params', flat=True), []) 
        return context

class ArticleFilterView(ListView):
    model = Article
    template_name = 'news/searched-articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(ArticleFilterView, self).get_queryset()
        query = self.request.GET.get('search_query')
        queryset = queryset.filter(Q(title__icontains = query) | Q(body__icontains = query)).select_related('category')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleFilterView, self).get_context_data(**kwargs)
        
        query = self.request.GET.get('search_query')
        categories = Category.objects.all()

        context['categories'] = categories
        context['query'] = query
        qs = self.get_queryset().exclude(video='')
        context['video'] = None
        if qs.exists():
            context['video'] = qs[0].video.url
        context['tags'] = sum(categories.exclude(search_params=None).values_list('search_params', flat=True), []) 

        return context

class ArticleDetail(View):
    def get(self, request, **kwargs):
        articles = Article.objects.all()
        categories = Category.objects.all()
        try:
            article = articles.get(slug=self.kwargs.get('article_slug'))
        except:
            raise Http404()
        
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        if not ArticleViews.objects.filter(article=article, ip=ip).exists():
            ArticleViews.objects.create(article=article, ip=ip)
            article.views += 1
            article.save()

        related_articles = article.category.articles.exclude(id=article.id)[:3]
        popular_articles = articles.filter(popular=True).exclude(id=article.id)[:4]
        query_tags = sum(Category.objects.exclude(search_params=None).values_list('search_params', flat=True), []) 

        context = {'articles': articles, 'article': article, 'related_articles': related_articles, 'popular_articles':popular_articles, 'tags':query_tags, 'categories':categories}
        return render(request, 'news/article-detail.html', context)
