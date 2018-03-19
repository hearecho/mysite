from django.shortcuts import render,render_to_response,get_object_or_404
from .models import Blog,BlogType
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.
#引入共用函数
from . import common_func


def blog_list(request):
    
    blogs_all = Blog.objects.all()
    
    # paginator = Paginator(blogs_all,Each_page_num)#分页器  10页
    # page_num = request.GET.get('page',1) #get 请求 ?page=1
    # page_of_blogs = paginator.get_page(page_num)

    # currentr_page_num = page_of_blogs.number#获取当前页码
    # page_range = common_func.Spilt_page(currentr_page_num,paginator)


    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    # context['blog_types'] = BlogType.objects.all()
    # context['page_of_blogs'] = page_of_blogs
    # context['page_range'] = page_range
    # context['blog_dates'] = Blog.objects.dates('created_time','month','DESC')
    return render_to_response('blog_list.html',context)
    

def blog_detail(request,blog_id):
    context = {}
    blog = get_object_or_404(Blog,pk = blog_id)
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    print(context['previous_blog'])
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['blog'] = blog

    return render_to_response('blog_detail.html',context)
    

def blogs_with_type(request,blog_type_id):
    blogs_all = Blog.objects.all().filter(blog_type=blog_type_id)
    
    # paginator = Paginator(blogs_all,Each_page_num)#分页器  10页
    # page_num = request.GET.get('page',1) #get 请求 ?page=1
    # page_of_blogs = paginator.get_page(page_num)

    # currentr_page_num = page_of_blogs.number#获取当前页码
    # page_range = common_func.Spilt_page(currentr_page_num,paginator)
    
    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['type'] = get_object_or_404(BlogType,pk = blog_type_id)
    # context['blog_types'] = BlogType.objects.all()
    # context['page_of_blogs'] = page_of_blogs
    # context['page_range'] = page_range
    return render_to_response('blogs_with_type.html',context)


def user_blogs(request,user_id):
    blogs_all = Blog.objects.all().filter(author=user_id)
    
    # paginator = Paginator(blogs_all,Each_page_num)#分页器  10页
    # page_num = request.GET.get('page',1) #get 请求 ?page=1
    # page_of_blogs = paginator.get_page(page_num)

    # currentr_page_num = page_of_blogs.number#获取当前页码
    # page_range = common_func.Spilt_page(currentr_page_num,paginator)

    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['user'] = get_object_or_404(User,pk=user_id)
    # context['blog_types'] = BlogType.objects.all()
    # context['page_of_blogs'] = page_of_blogs
    # context['page_range'] = page_range
    return render_to_response('user_blogs.html',context)


def blogs_with_date(request,year,month):
    blogs_all = Blog.objects.filter(created_time__year=year,created_time__month=month)
    
    # paginator = Paginator(blogs_all,Each_page_num)#分页器  10页
    # page_num = request.GET.get('page',1) #get 请求 ?page=1
    # page_of_blogs = paginator.get_page(page_num)

    # currentr_page_num = page_of_blogs.number#获取当前页码
    # page_range = common_func.Spilt_page(currentr_page_num,paginator)


    context = {}
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['blogs_with_date'] = "{}年{}月".format(year,month)
    # context['blog_types'] = BlogType.objects.all()
    # context['page_of_blogs'] = page_of_blogs
    # context['page_range'] = page_range
    # context['blog_dates'] = Blog.objects.dates('created_time','month','DESC')
    return render_to_response('blogs_with_date.html',context)
    