from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    comment_form = CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        #返回数据
        data['status'] = "SUCCESS"
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")
        data['text'] = comment.text
    else:
        # return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
        data['status'] = 'ERROR'
        data['message'] = comment_form.errors
    return JsonResponse(data)