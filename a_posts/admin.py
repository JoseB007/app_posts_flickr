from django.contrib import admin

from .models import Post, Tag, Comment, Reply, LikedPosts

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["creation_date", "author_full_name", "title"]

    @admin.display(description="Autor")
    def author_full_name(self, obj):
        return obj.get_author()['full_name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["creation_date", "post", "author_full_name"]

    @admin.display(description="Autor")
    def author_full_name(self, obj):
        return obj.author.profile.get_full_name()


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ["creation_date", "author_full_name", "post_comment"]

    @admin.display(description="Comentario")
    def post_comment(self, obj):
        return f"Comentario de {obj.comment.author.profile.get_full_name()} en {obj.comment.post}"
    
    @admin.display(description="Autor")
    def author_full_name(self, obj):
        return obj.author.profile.get_full_name()


@admin.register(LikedPosts)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ["created", "post", "author_full_name"]
    list_filter = ["post"]

    @admin.display(description="Autor")
    def author_full_name(self, obj):
        return obj.user.profile.get_full_name()


admin.site.register(Tag)