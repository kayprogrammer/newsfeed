from django.shortcuts import get_object_or_404, render
from django.views import View

from news.models import Article, Category
# Create your views here.

class HomeView(View):
    def get(self, request):
        articles = Article.objects.all()
        categories = Category.objects.all()

        context = {'article': articles, 'categories':categories}
        return render(request, 'news/home.html', context)

class AllArticlesView(View):
    def get(self, request):
        articles = Article.objects.all()

        context = {'article': articles}
        return render(request, 'news/home.html', context)

class ArticleDetail(View):
    def get(self, request, **kwargs):
        article = get_object_or_404(Article, slug=kwargs.get('article_slug'))
        related_articles = article.category.articles.exclude(id=article.id)

        context = {'article': article, 'related_articles': related_articles}
        return render(request, 'news/detail.html', context)
