from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('all-articles/', views.AllArticlesView.as_view(), name="all-articles"),
    path('all-articles/results/', views.ArticleFilterView.as_view(), name="searched-articles"),
    path('categories/<slug:category_slug>/', views.CategoryArticlesView.as_view(), name="category-articles"),
    path('all-articles/<slug:article_slug>/', views.ArticleDetail.as_view(), name="article-detail")

    
]