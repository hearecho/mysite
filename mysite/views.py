from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_count.utils import get_seven_readNum
from blog.models import Blog

def index(request):
    context = {}
    blog_contentType = ContentType.objects.get_for_model(Blog)
    dates,read_nums= get_seven_readNum(blog_contentType)

    context['read_nums'] = read_nums
    context['dates'] = dates
    return render_to_response("home.html",context)
    