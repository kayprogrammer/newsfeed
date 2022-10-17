from django.contrib import admin
from . models import Article, ArticleViews, Category

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'views']
    list_filter = ['title', 'category', 'status', 'views']
    search_fields = ['title', 'category', 'status']

    fieldsets = (
        ('General', {'fields': ['title', 'slug', 'body', 'category', 'image', 'video']}),
        ('Checks', {'fields': ['status', 'views', 'timestamp', 'modified']}),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ['name', ]
    search_fields = ['name', ]

    fieldsets = (
        ('General', {'fields': ['name', 'search_params', 'timestamp']}),
    )

class ArticleViewsAdmin(admin.ModelAdmin):
    list_display = ['article', 'ip', 'timestamp']
    list_filter = ['article', 'ip', 'timestamp']
    search_fields = ['article', 'ip']

    fieldsets = (
        ('General', {'fields': ['article', 'ip', 'timestamp']}),
    )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ArticleViews, ArticleViewsAdmin)
