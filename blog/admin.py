from django.contrib import admin
from .models import Post, Contact, Comment, Category
from datetime import datetime
from django.utils.html import format_html


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'is_solved', 'days', 'created_at')
    list_display_links = ('id', 'full_name')

    def days(self, obj):
        days_diff = (datetime.now() - obj.created_at).days
        if days_diff > 3:
            color = 'red'
        else:
            color = 'blue'
        if obj.is_solved:
            color = 'green'
        return format_html("<div style='color: {}'>{}</div>", color, days_diff)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview_image', 'author', 'category', 'is_published', 'view_count', 'created_at')
    list_display_links = ('id', 'title')
    inlines = (CommentInline,)
    search_fields = ('title', 'author')
    list_filter = ('author', 'is_published')

    def preview_image(self, obj):
        return format_html("<img height=30 src={}>", obj.image.url)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_visible', 'created_at')
    list_display_links = ('id', 'name')


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('id', 'title', 'is_published')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')
    inlines = (PostInline,)

# admin.site.register(Post, PostAdmin)
# admin.site.register(Contact, ContactAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Category, CategoryAdmin)
