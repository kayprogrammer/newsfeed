from django.shortcuts import redirect, render
from django.views import View
from news.models import Article
from others.forms import MessageForm
import sweetify

# Create your views here.

class ContactPageView(View):
    def get(self, request):
        popular_articles = Article.objects.filter(popular=True).select_related('category')[:5]
        form = MessageForm()
        context = {'form': form, 'popular_articles': popular_articles}
        return render(request, 'others/contact.html', context)

    def post(self, request):
        form = MessageForm()
        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                form.save()
                sweetify.success(request, title="Sent", text="Message was received and will be responded in due time. Thank you. ", icon="success", button="Ok", timer=4000)
                return redirect('/others/contact/')
            else:
                sweetify.error(request, title="Something went wrong", text="Please try again later, Thank you.", icon="error", button="Ok", timer=4000)
                return redirect('/others/contact/')
        context = {'form': form}
        return render(request, 'others/contact.html', context)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)