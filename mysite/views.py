from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_count.utils import get_seven_readNum,get_today_hot_data,get_yseterday_hot_data,get_week_hot_date,get_month_hot_date
from blog.models import Blog


def index(request):
    context = {}
    blog_contentType = ContentType.objects.get_for_model(Blog)
    dates,read_nums= get_seven_readNum(blog_contentType)
    today_hot_data = get_today_hot_data(blog_contentType)
    yesterday_hot_data = get_yseterday_hot_data(blog_contentType)

    # 缓存的设置存取
    # 获取week_hot_data 缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_week_hot_date()
        cache.set('week_hot_data',week_hot_data,3600)#3600s  一个小时
    else:
        print("use cache")

    # 获取month_hot_data 缓存数据
    month_hot_data = cache.get('month_hot_data')
    if month_hot_data is None:
        month_hot_data = get_month_hot_date()
        cache.set('month_hot_data', month_hot_data, 3600)  # 3600s  一个小时


    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['week_hot_data'] = week_hot_data
    context['month_hot_data'] = month_hot_data
    return render_to_response("home.html",context)
    