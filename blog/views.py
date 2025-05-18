from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView,DetailView
from . models import Post, Category, Tag, Like,Comment,CommentLike
from . forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'blog/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(status='P').order_by('-created')[:6]
        context['post_title'] = 'Latest posts'
        
        return context




class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status = 'P').order_by('-created')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All posts'
        context['page1_title'] = 'Blog'  
        context['categories'] = Category.objects.all() 
        
        return context 
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def get_queryset(self):
        return Post.objects.filter(status = 'P').prefetch_related('tags')
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'PostDetail'
        context['form'] = CommentForm()  # فرم خالی برای نمایش
      # فقط کامنت‌های تایید شده + بهینه شده با یوزر
        context['comments'] = self.object.comments.filter(
            status='A', parent__isnull=True
        ).select_related('user').prefetch_related(
            Prefetch(
    'replies',
    queryset=Comment.objects.filter(status='A').select_related('user').annotate(like_count=Count('likes'))
)
        ).annotate(like_count=Count('likes'))
        
        
        

        if self.request.user.is_authenticated:
            context['has_liked'] = self.object.likes.filter(user=self.request.user).exists()
        else:
            context['has_liked'] = False
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.parent = form.cleaned_data.get('parent')
            comment.save()
            return redirect(self.get_success_url())
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            # اگه لاگین بود بفرستش روی صفحه جزئیات پست
            return reverse('PostDetail', kwargs={'slug': self.object.slug})
        else:
            # اگه لاگین نبود، بفرستش به صفحه لاگین
            return reverse('login')
class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(status='P', category=self.category).order_by('-created')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Category: {self.category.name}"
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.category
        return context
    
    
    
    
class TagPostListView(ListView):
    model=Post
    template_name='blog/tags_list.html'
    context_object_name ='posts'
    paginate_by = 4

    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        return Post.objects.filter(status='P', tags=self.tag).order_by('-created')
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Tag: {self.tag.name}"
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.tag
        return context
    
    
@require_POST
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='P')

    
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        # اگر قبلا لایک کرده بود، آنلایک کنیم
        like.delete()

    return redirect('PostDetail', slug=slug)
    

@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # بررسی وجود لایک قبلی
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        like.delete()  # اگر قبلاً لایک کرده، حذفش کن (آن‌لایک)

    # ریدایرکت به جزئیات پست
    return redirect('PostDetail', slug=comment.post.slug)
