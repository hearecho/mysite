from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Comment
from mysite.deal_error import deal_error
# Create your views here.

def update_comment(request):

    # 数据检查
    if not request.user.is_authenticated:
        # deal_error(request,"用户未登陆")
        return render(request, 'error.html', {'message': '用户未登陆'})
    text = request.POST.get('text','').strip()
    if text=="":
        # deal_error(request,"评论内容为空")
        return render(request, 'error.html', {'message':'评论内容为空'})

    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id',''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        # deal_error(request,"评论对象不存在"+"\n"+e.args)
        return render(request, 'error.html', {'message': "评论对象不存在"+"\n"+e.args})

    # 检查通过后存储
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    #
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(referer)

