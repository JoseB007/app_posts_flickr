from django import template
from django.db.models import Count

from a_posts.models import Post, Tag

register = template.Library()

@register.inclusion_tag("includes/sidebar.html")
def sidebar_view(current_tag=None, *args, **kargs):
    tags = Tag.objects.all()
    top_posts = Post.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')[:3]
    context = {
        'categories': tags,
        'current_tag': current_tag,
        'top_posts': top_posts,
    }
    return context