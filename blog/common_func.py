from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.contrib.auth.models import User
#公用函数
Each_page_num = 4


def Spilt_page(currentr_page_num,paginator):
    a = list(range(max(currentr_page_num-2,1),currentr_page_num))
    b = list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages) + 1))
    page_range = a+b

    #加上省略页码标记
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    
    # 首页尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    return page_range


def get_blogs_common_list(request,blogs_all):
    context = {}

    paginator = Paginator(blogs_all,Each_page_num)#分页器  10页
    page_num = request.GET.get('page',1) #get 请求 ?page=1
    page_of_blogs = paginator.get_page(page_num)

    currentr_page_num = page_of_blogs.number#获取当前页码
    a = list(range(max(currentr_page_num-2,1),currentr_page_num))
    b = list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages) + 1))
    page_range = a+b

    #加上省略页码标记
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    
    # 首页尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context['blog_types'] = BlogType.objects.all()
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time','month','DESC')


    return context