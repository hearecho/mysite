from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "blog"
urlpatterns = [
    #列表 http://loclhost:8000/blog/
    path('',views.blog_list,name = "blog_list"),
    #blog详情页 http://localhost:8000/blog/1
    path('<int:blog_id>',views.blog_detail,name = "blog_detail"),

    #blog_with_type 的blog文章列表页
    path('type/<int:blog_type_id>',views.blogs_with_type,name="blogs_with_type"),

    #user_blogs 个人的blog列表
    path('user/<int:user_id>',views.user_blogs,name="user_blogs"),

    #按月份 分类
    path('date/<int:year>/<int:month>',views.blogs_with_date,name = "blogs_with_date")
]
