from django.shortcuts import render,render_to_response,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from .models import Blog,BlogType
from read_count.models import ReadNum
# Create your views here.
#引入共用函数
from . import common_func
from read_count.utils import read_count_once_read


def blog_list(request):
    
    blogs_all = Blog.objects.all()
    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    return render_to_response('blog_list.html',context)
    

def blog_detail(request,blog_id):
    
    blog = get_object_or_404(Blog,pk = blog_id)
    read_count_once_read(request,blog)

    
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['blog'] = blog

    response = render_to_response('blog_detail.html',context)
    response.set_cookie('blog_{}_readed'.format(blog_id),'true')
    return response
    

def blogs_with_type(request,blog_type_id):
    blogs_all = Blog.objects.all().filter(blog_type=blog_type_id)
    
    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['type'] = get_object_or_404(BlogType,pk = blog_type_id)
    return render_to_response('blogs_with_type.html',context)


def user_blogs(request,user_id):
    blogs_all = Blog.objects.all().filter(author=user_id)

    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['user'] = get_object_or_404(User,pk=user_id)
    return render_to_response('user_blogs.html',context)


def blogs_with_date(request,year,month):
    blogs_all = Blog.objects.filter(created_time__year=year,created_time__month=month)

    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['blogs_with_date'] = "{}年{}月".format(year,month)
    return render_to_response('blogs_with_date.html',context)
    