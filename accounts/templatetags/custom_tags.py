from django import template
from others.models import About
from news.models import Article, Category

register = template.Library()

@register.inclusion_tag('news/header-data.html', takes_context=True)
def header_data(context):
    try:
        site = About.objects.get()
    except About.DoesNotExist:
        site = About.objects.create(name="NewsFeed") 
    tags = Category.objects.all()

    articles = Article.objects.all()[:10]
    return {'site': site, 'categories':tags, 'articles':articles,'request':context.get('request')}

@register.inclusion_tag('news/footer-data.html', takes_context=True)
def footer_data(context):
    try:
        site = About.objects.get()
    except About.DoesNotExist:
        site = About.objects.create(name="NewsFeed") 
    tags = Category.objects.all()
    return {'site': site, 'categories':tags, 'request':context.get('request')}

def arithmetic_progression(a, d, l):
    #a = first term, #d = common difference, #l = limit
    return list(range(a, l + 1, d))

@register.filter
def check_if_in_progression(counter):
    # Our category save method confirms that we have less than 10 categories or else 30 as limit would not be enough. Think about it 😉

    if counter in arithmetic_progression(1, 3, 30):
        return True
    else:
        return False

@register.filter
def subtract(value, subtrahend):
    return (value - subtrahend)