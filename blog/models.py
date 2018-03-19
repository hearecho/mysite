from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
                                                            


class Blog(models.Model):
    title = models.CharField(max_length=30,unique=True)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    #外键
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)

    def __str__(self):#解决content过长占用位置大的问题
        # if len(self.content)>40:
        #     return "{} ...".format(self.content[0:39])
        # else:
        #     return self.content
        return '<Blog : {}>'.format(self.title)


    class Meta:
        ordering = ["-last_updated_time"]


