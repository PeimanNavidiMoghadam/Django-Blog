from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published', 'category')
    list_filter = ('status', 'created', 'category', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # پر کردن خودکار اسلاگ از عنوان
    raw_id_fields = ('author',)
    date_hierarchy = 'published'
    ordering = ('-published',)
    filter_horizontal = ('tags',)  # برای انتخاب چندتایی تگ‌ها


# admin.p

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # در صفحه لیست ادمین این فیلدها نمایش داده میشن
    prepopulated_fields = {'slug': ('name',)}  # هنگام نوشتن عنوان، اسلاگ خودش ساخته میشه


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # فیلدهایی که توی لیست نشون داده میشن
    prepopulated_fields = {'slug': ('name',)}  # موقع وارد کردن عنوان، اسلاگ اتوماتیک ساخته میشه



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('user__username', 'post__title', 'body')
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status=Comment.Status.APPROVED)
    approve_comments.short_description = 'تایید کامنت‌های انتخاب شده'

    def reject_comments(self, request, queryset):
        queryset.update(status=Comment.Status.REJECTED)
    reject_comments.short_description = 'رد کردن کامنت‌های انتخاب شده'