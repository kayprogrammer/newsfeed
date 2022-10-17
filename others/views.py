from django.shortcuts import render
from django.views import View

from others.models import About

# Create your views here.

# class SiteDetail(View):
#     def get(self, request):
#         try:
#             site = About.objects.get()
#         except About.DoesNotExist:
#             site = About.objects.create(name="NewsFeed") 
        
#         context = {'site': site}
#         return render(request, 'others/contact.html', context)

class MessageView(View):
    def post(self, request):
        try:
            site = About.objects.get()
        except About.DoesNotExist:
            site = About.objects.create(name="NewsFeed") 
        
        context = {'site': site}
        return render(request, 'others/contact.html', context)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)