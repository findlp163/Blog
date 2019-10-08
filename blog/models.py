from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from markdown import Markdown


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_category'  # 自定义表名
        verbose_name = '分类'  # 可读的中文名字
        verbose_name_plural = verbose_name  # 指定模型的复数形式


# 文章
class Post(models.Model):
    title = models.CharField(max_length=100)  # 标题
    body = RichTextUploadingField(config_name='default')  # 内容

    created_time = models.DateTimeField(default=timezone.now)  # 创建时间
    modified_time = models.DateTimeField(default=timezone.now)  # 更新时间

    excerpt = models.CharField(max_length=200, blank=True)  # 摘要

    category = models.ForeignKey(Category)  # 分类

    author = models.ForeignKey(User)  # 作者
    views = models.PositiveIntegerField(default=0)  # 阅读量

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time', 'title']  # 以created_time降序,以title升序
        db_table = 'tb_post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Blogroll(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_blogroll'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class Blogger(models.Model):
    contact_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.contact_name

    class Meta:
        db_table = 'tb_blogger'
        verbose_name = '关于我'
        verbose_name_plural = verbose_name
