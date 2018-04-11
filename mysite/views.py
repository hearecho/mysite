from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse

from read_count.utils import get_seven_readNum,get_today_hot_data,get_yseterday_hot_data,get_week_hot_date,get_month_hot_date
from django.shortcuts import render,redirect
from blog.models import Blog

from .forms import LoginForm,RegForm
from django.contrib.auth.models import User

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
        # print("use cache")
        pass
    # 获取month_hot_data 缓存数据
    month_hot_data = cache.get('month_hot_data')
    if month_hot_data is None:
        month_hot_data = get_month_hot_date()
        cache.set('month_hot_data', month_hot_data, 3600)  # 3600s  一个小时

    login_form = LoginForm()
    context['login_form'] = login_form

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['week_hot_data'] = week_hot_data
    context['month_hot_data'] = month_hot_data
    return render(request, "home.html", context)


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #验证操作在forms文件里面
            user = login_form.cleaned_data['user']
            # 请求来源 get
            login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    context = {}
    return render(request,'home.html',context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            #验证操作在forms文件里面
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            #存储数据库
            user = User.objects.create_user(username,email,password)
            user.save()
            # 注册后登陆
            user = authenticate(username=username,password=password)
            login(request,user)
            # 请求来源 get

            return redirect(request.GET.get('from',reverse('home')))
    context = {}
    return render(request,'home.html',context)

def logout(request):#暂时的登出

    request.session.flush()

    return redirect('/')




