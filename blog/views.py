from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from blog.models import Post, Category, Blogroll, Blogger
from comments.forms import CommentForm


class IndexView(ListView):
    """主页"""
    model = Post  # 指定model模型是Post
    template_name = 'index.html'  # 指定这个视图渲染的模板
    context_object_name = 'post_list'  # 指定获取的模型列表数据保存的变量名,这个变量会被传递给模板
    paginate_by = 5  # 分页

    def get_context_data(self, **kwargs):  # 添加额外的参数传递给模板
        context = super(IndexView, self).get_context_data(**kwargs)
        post_list_hot = Post.objects.order_by('-views')[:5]  # 获取前五个热门
        blogroll_list = Blogroll.objects.all()  # 友情链接
        contact_list = Blogger.objects.all()  # 作者联系方式
        context.update({
            'post_list_hot': post_list_hot,
            'blogroll_list': blogroll_list,
            'contact_list': contact_list,
        })
        return context


class CategotysPostView(IndexView):
    """主页-分类"""

    def get_queryset(self):  # 默认获取指定模型的全部列表数据,这里进行覆写
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))  # 过滤获取
        return super(CategotysPostView, self) \
            .get_queryset().filter(category=cate)


class ArchivesPost(IndexView):
    """主页-归档"""

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesPost, self) \
            .get_queryset().filter(created_time__year=year,
                                   created_time__month=month)


class DetailPostView(DetailView):
    """详情页"""
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):  # 覆写 get方法,为了将文章阅读量 +1
        response = super(DetailPostView, self).get(request, *args, **kwargs)

        # 将文章阅读量+1
        self.object.increase_views()

        # get 方法必须返回 HttpResponse实例
        return response

    # def get_object(self, queryset=None):  # 覆写 get_object方法为了对 post的 body值进行渲染
    #     post = super(DetailPostView, self).get_object(queryset=None)
    #     post.body = markdown(post.body,
    #                          extensions=[
    #                              'markdown.extensions.extra',
    #                              'markdown.extensions.codehilite',
    #                              'markdown.extensions.toc',
    #                          ])
    #     return post

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        post_list_hot = Post.objects.order_by('-views')[:5]
        blogroll_list = Blogroll.objects.all()
        contact_list = Blogger.objects.all()

        form = CommentForm()
        # 获取文章下所以评论,并倒序
        comment_list = self.object.comment_set.order_by('-created_time')
        context.update({
            'post_list_hot': post_list_hot,
            'blogroll_list': blogroll_list,
            'contact_list': contact_list,
            'form': form,
            'comment_list': comment_list
        })
        return context


class CategoryView(ListView):
    """分类页"""
    model = Category
    template_name = 'category.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_list = Category.objects.annotate(num_posts=Count('post'))
        post_list_hot = Post.objects.order_by('-views')[:5]
        blogroll_list = Blogroll.objects.all()
        contact_list = Blogger.objects.all()
        context.update({
            'category_list': category_list,
            'post_list_hot': post_list_hot,
            'blogroll_list': blogroll_list,
            'contact_list': contact_list,
        })
        return context


class ArchivesView(ListView):
    """归档页"""
    model = Category
    template_name = 'archives.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        date_list = Post.objects.dates('created_time', 'month', order='DESC')

        post_list_hot = Post.objects.order_by('-views')[:5]
        blogroll_list = Blogroll.objects.all()
        contact_list = Blogger.objects.all()
        context.update({
            'date_list': date_list,
            'post_list_hot': post_list_hot,
            'blogroll_list': blogroll_list,
            'contact_list': contact_list,
        })
        return context


# 简单搜索功能  Q对象
def search(request):
    q = request.GET.get('q')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    post_list_hot = Post.objects.order_by('-views')[:5]
    blogroll_list = Blogroll.objects.all()
    contact_list = Blogger.objects.all()

    context = {
        'post_list': post_list,
        'post_list_hot': post_list_hot,
        'blogroll_list': blogroll_list,
        'contact_list': contact_list,
    }
    return render(request, 'index.html', context=context)
