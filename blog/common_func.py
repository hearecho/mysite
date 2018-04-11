from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Count
from mysite.forms import LoginForm,RegForm
#公用函数
Each_page_num = 4

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

    #获取类别blog各个类别的数量
    #第一种方法
    # BlogType.objects.annotate(blog_count=Count('blog'))

    #第二种方法
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type = blog_type).count()
        blog_types_list.append(blog_type)
    '''
    #context['blog_types'] = blog_types_list
    #获取日期归档的blog数量
    blog_dates = Blog.objects.dates('created_time','month','DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    #第二种方法仍是使用 annotate方法 不一样的是 是使用
    #db = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month)
    #db.annotate


    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict

    return context

def pro_loginform_template(request):
    login_form = LoginForm()
    reg_form = RegForm()

    return {'login_form':login_form,'reg_form':reg_form}