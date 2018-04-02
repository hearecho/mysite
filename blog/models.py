from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_count.models import ReadNumExpandMethod,ReadDetail
# Create your models here.



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
                                                            


class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=30,unique=True)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    #外键
    read_details =GenericRelation(ReadDetail)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)



    def __str__(self):#解决content过长占用位置大的问题
        return '<Blog : {}>'.format(self.title)


    class Meta:
        ordering = ["-last_updated_time"]



