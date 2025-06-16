from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import CommentForm
from django.core.paginator import Paginator
# Create your views here.


def news_list(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 4)  # по 4 новини на сторінку

    page_number = request.GET.get('page')
    news_items = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'news_items': news_items})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    comments = news.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            return redirect('news_detail', slug=news.slug)

    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })