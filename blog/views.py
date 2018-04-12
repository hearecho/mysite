from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .models import Blog,BlogType
from django.contrib.contenttypes.models import ContentType
# Create your views here.
#引入共用函数
from . import common_func
from read_count.utils import read_count_once_read
from comment.models import Comment
from comment.forms import CommentForm


def blog_list(request):
    
    blogs_all = Blog.objects.all()
    context = common_func.get_blogs_common_list(request,blogs_all)
    return render(request,'blog_list.html',context)
    

def blog_detail(request,blog_id):
    
    blog = get_object_or_404(Blog,pk = blog_id)
    read_count_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.id)
    
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_id})
    response = render(request,'blog_detail.html',context)
    response.set_cookie('blog_{}_readed'.format(blog_id),'true',3600)#设置cookie标记 防止每次点击文章都会增加一次阅读记录
    return response
    

def blogs_with_type(request,blog_type_id):
    blogs_all = Blog.objects.all().filter(blog_type=blog_type_id)

    context = common_func.get_blogs_common_list(request,blogs_all)
    context['type'] = get_object_or_404(BlogType,pk = blog_type_id)
    return render(request,'blogs_with_type.html',context)


def user_blogs(request,user_id):
    blogs_all = Blog.objects.all().filter(author=user_id)
    context = common_func.get_blogs_common_list(request,blogs_all)
    context['user'] = get_object_or_404(User,pk=user_id)
    return render(request,'user_blogs.html',context)


def blogs_with_date(request,year,month):
    blogs_all = Blog.objects.filter(created_time__year=year,created_time__month=month)

    context = common_func.get_blogs_common_list(request,blogs_all)
    context['blogs_with_date'] = "{}年{}月".format(year,month)
    return render(request,'blogs_with_date.html',context)
    