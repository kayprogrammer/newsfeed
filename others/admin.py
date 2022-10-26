from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from . models import About, Message

# Register your models here.

class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ['name', 'email', 'phone', 'address', 'desc', 'timestamp']}),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return HttpResponseRedirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))
        return super(AboutAdmin, self).changelist_view(request=request, extra_context=extra_context)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'addressed', 'timestamp']
    list_filter = ['name', 'email', 'addressed', 'timestamp']
    search_fields = ['name', 'email', 'addressed', 'timestamp']

    fieldsets = (
        ('General', {'fields': ['name', 'email', 'body', 'addressed', 'timestamp']}),
    )

    def has_add_permission(self, request):
        return False

admin.site.site_header = mark_safe('<strong style="font-weight:bold;">NEWSFEED ADMIN</strong>')
admin.site.register(About, AboutAdmin)
admin.site.register(Message, MessageAdmin)
