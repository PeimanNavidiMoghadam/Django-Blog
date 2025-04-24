from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from . models import Post

class HomeView(TemplateView):
    template_name = 'blog/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(status='P').order_by('-created')[:6]
        return context
