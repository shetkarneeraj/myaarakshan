from django.shortcuts import render
from django.core.paginator import Paginator
from .models import News


def news_list(request):
    """News list page with pagination"""
    page = request.GET.get('page', 1)
    news_queryset = News.objects.order_by('-date_posted')
    
    paginator = Paginator(news_queryset, 10)
    news_items = paginator.get_page(page)
    
    return render(request, 'news.html', {'news_items': news_items})