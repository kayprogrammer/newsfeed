from django.contrib import admin
from django.utils import timezone
from . models import Article, ArticleViews, Category

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'popular', 'views']
    list_filter = ['title', 'category', 'popular', 'views']
    search_fields = ['title', 'category', 'popular']
    readonly_fields = ["admin", "modified", "views", 'timestamp']

    fieldsets = (
        ('General', {'fields': ['admin', 'title', 'body', 'category', 'image', 'video']}),
        ('Checks', {'fields': ['popular', 'slider','views', 'timestamp', 'modified']}),
    )

    def save_model(self, request, obj, form, change):
        if obj.admin != None: # Just to check if this is an update request cos admin is none when creating
            obj.modified = timezone.now()
        else: # setting obj admin during creation only 
            obj.admin = request.user
        obj.save()

    def render_change_form(self, request, context, obj, add=False, change=False, form_url=''):
        if not '/add/' in request.path:
            # Allow only super users and article owner to update article
            if request.user != obj.admin and request.user.is_superuser != True:
                context.update({
                    'show_save': False,
                    'show_save_and_continue': False,
                    'show_delete': False,
                    'show_save_and_add_another': False
                })
        return super().render_change_form(request, context, add, change, form_url, obj)

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
